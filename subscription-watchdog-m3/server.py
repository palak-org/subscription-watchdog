from mcp.server.fastmcp import FastMCP
from db import get_connection
import os
import datetime
from decimal import Decimal

# Initialize FastMCP Server
mcp = FastMCP("subscription-watchdog-m3")

def serialize_value(val):
    """Helper to convert database types to JSON-serializable types."""
    if isinstance(val, Decimal):
        return float(val)
    elif isinstance(val, (datetime.datetime, datetime.date)):
        # Format date/datetime as ISO strings.
        # If it's a timezone-aware datetime, replace standard +00:00 with Z for consistency
        iso_str = val.isoformat()
        if iso_str.endswith("+00:00"):
            iso_str = iso_str[:-6] + "Z"
        return iso_str
    return val

def serialize_dict(row):
    """Helper to serialize all values in a dictionary row."""
    if not row:
        return row
    return {k: serialize_value(v) for k, v in row.items()}

@mcp.tool()
def add_sub(
    merchant_name: str,
    price: float,
    currency: str,
    billing_cycle: str,
    detected_date: str,
    user_id: str,
    confidence: float,
    category: str,
    is_recurring: bool,
    raw_description: str = ""
) -> dict:
    """
    Add a new subscription or update an existing one. If the price changes,
    a record is inserted into the price history table.
    
    Parameters:
    - merchant_name: The name of the merchant (e.g. "Netflix")
    - price: The subscription price (e.g. 15.49)
    - currency: Currency code (e.g. "USD")
    - billing_cycle: Cycle of billing ('monthly', 'yearly', 'weekly')
    - detected_date: The date detected in YYYY-MM-DD format
    - user_id: ID of the user owning the subscription
    - confidence: Confidence score of the detection (0.0 to 1.0)
    - category: Category of subscription (e.g. 'streaming', 'saas')
    - is_recurring: True if recurring subscription, False otherwise
    - raw_description: The raw text matching the transaction description (optional)
    """
    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                # 1. Check if a subscription already exists for this user + merchant
                cur.execute(
                    """
                    SELECT id, price, currency FROM subscriptions
                    WHERE user_id = %s AND merchant_name = %s
                    """,
                    (user_id, merchant_name)
                )
                existing = cur.fetchone()
                
                if not existing:
                    # 2. Insert new row
                    cur.execute(
                        """
                        INSERT INTO subscriptions (
                            user_id, merchant_name, raw_description, price, currency,
                            billing_cycle, detected_date, confidence, category, is_recurring
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        RETURNING id
                        """,
                        (
                            user_id, merchant_name, raw_description, Decimal(str(price)), currency,
                            billing_cycle, detected_date, Decimal(str(confidence)), category, is_recurring
                        )
                    )
                    sub_id = cur.fetchone()['id']
                    return { "action": "created", "sub_id": str(sub_id) }
                
                existing_id = existing['id']
                existing_price = existing['price']
                incoming_price = Decimal(str(price))
                
                if existing_price != incoming_price:
                    # 3. Insert into price_history and update subscription
                    cur.execute(
                        """
                        INSERT INTO price_history (
                            subscription_id, old_price, new_price, currency
                        ) VALUES (%s, %s, %s, %s)
                        RETURNING change_pct
                        """,
                        (existing_id, existing_price, incoming_price, currency)
                    )
                    change_pct = cur.fetchone()['change_pct']
                    
                    cur.execute(
                        """
                        UPDATE subscriptions SET
                            price = %s,
                            currency = %s,
                            billing_cycle = %s,
                            detected_date = %s,
                            confidence = %s,
                            category = %s,
                            is_recurring = %s,
                            raw_description = %s,
                            updated_at = NOW()
                        WHERE id = %s
                        """,
                        (
                            incoming_price, currency, billing_cycle, detected_date,
                            Decimal(str(confidence)), category, is_recurring, raw_description, existing_id
                        )
                    )
                    
                    return {
                        "action": "price_updated",
                        "sub_id": str(existing_id),
                        "old_price": float(existing_price),
                        "new_price": float(incoming_price),
                        "change_pct": float(change_pct) if change_pct is not None else 0.0
                    }
                else:
                    # 4. Price is the same: update updated_at and other fields
                    cur.execute(
                        """
                        UPDATE subscriptions SET
                            currency = %s,
                            billing_cycle = %s,
                            detected_date = %s,
                            confidence = %s,
                            category = %s,
                            is_recurring = %s,
                            raw_description = %s,
                            updated_at = NOW()
                        WHERE id = %s
                        """,
                        (
                            currency, billing_cycle, detected_date, Decimal(str(confidence)),
                            category, is_recurring, raw_description, existing_id
                        )
                    )
                    return { "action": "refreshed", "sub_id": str(existing_id) }
    finally:
        conn.close()

@mcp.tool()
def get_subs(
    user_id: str,
    status: str = "active",
    category: str = "",
    min_confidence: float = 0.0
) -> list:
    """
    Get all subscriptions matching the criteria for a specific user.
    Includes the latest previous price if a price change occurred.
    
    Parameters:
    - user_id: ID of the user (required)
    - status: 'active', 'cancelled', or 'all' to skip filter
    - category: optional category filter (e.g. 'streaming', 'saas')
    - min_confidence: optional confidence threshold (0.0 to 1.0)
    """
    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                # Query subscription table joined with latest price history
                query = """
                    SELECT s.id, s.user_id, s.merchant_name, s.raw_description, s.price, s.currency,
                           s.billing_cycle, s.detected_date, s.confidence, s.category, s.is_recurring,
                           s.status, s.flagged, s.flag_detail, s.created_at, s.updated_at,
                           ph.old_price AS prev_price
                    FROM subscriptions s
                    LEFT JOIN LATERAL (
                        SELECT old_price
                        FROM price_history
                        WHERE subscription_id = s.id
                        ORDER BY changed_at DESC
                        LIMIT 1
                    ) ph ON TRUE
                    WHERE s.user_id = %s
                """
                params = [user_id]
                
                if status != "all":
                    query += " AND s.status = %s"
                    params.append(status)
                    
                if category:
                    query += " AND s.category = %s"
                    params.append(category)
                    
                if min_confidence > 0.0:
                    query += " AND s.confidence >= %s"
                    params.append(Decimal(str(min_confidence)))
                    
                query += " ORDER BY s.updated_at DESC"
                
                cur.execute(query, tuple(params))
                rows = cur.fetchall()
                return [serialize_dict(row) for row in rows]
    finally:
        conn.close()

@mcp.tool()
def flag_sub(
    sub_id: str,
    reason: str,
    detail: str,
    user_id: str
) -> dict:
    """
    Flag a subscription with a specific reason.
    
    Parameters:
    - sub_id: UUID of the subscription to flag
    - reason: 'price_spike', 'unused', 'duplicate', 'trial_ending'
    - detail: human-readable explanation of why it was flagged
    - user_id: user ID of the owner (for ownership validation)
    """
    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                # 1. Verify existence and ownership
                cur.execute(
                    "SELECT id FROM subscriptions WHERE id = %s AND user_id = %s",
                    (sub_id, user_id)
                )
                existing = cur.fetchone()
                if not existing:
                    return { "error": "subscription not found" }
                
                # 2. Update status and flagging details
                cur.execute(
                    """
                    UPDATE subscriptions SET
                        flagged = %s,
                        flag_detail = %s,
                        updated_at = NOW()
                    WHERE id = %s AND user_id = %s
                    """,
                    (reason, detail, sub_id, user_id)
                )
                
                return {
                    "action": "flagged",
                    "sub_id": str(sub_id),
                    "reason": reason,
                    "detail": detail
                }
    finally:
        conn.close()

if __name__ == "__main__":
    import sys
    # When debugging or inspecting, FastMCP can run using stdio
    # But by default, if run directly, it will run as streamable-http as required.
    mcp.run(transport="streamable-http", host="0.0.0.0", port=8000)
