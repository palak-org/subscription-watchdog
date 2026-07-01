



from database.db import get_connection, init_db

init_db()


def load_memory():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT name, amount, currency FROM subscriptions")
    rows = cursor.fetchall()

    conn.close()

    memory = []
    for row in rows:
        memory.append({
            "name": row["name"],
            "amount": row["amount"],
            "currency": row["currency"]
        })

    return memory


def save_memory(subscriptions):
    conn = get_connection()
    cursor = conn.cursor()

    for sub in subscriptions:
        cursor.execute("""
            INSERT INTO subscriptions (name, amount, currency)
            VALUES (?, ?, ?)
        """, (sub["name"], sub["amount"], sub["currency"]))

    conn.commit()
    conn.close()
