import requests
from src.phase2.agents.classifier_agent import ClassifierAgent
from src.phase2.agents.extractor_agent import ExtractorAgent

def map_category(cat):
    mapping = {
        "Entertainment": "streaming",
        "Music": "streaming",
        "Video": "streaming",

        "Software": "saas",
        "AI": "saas",
        "SaaS": "saas",

        "Fitness": "fitness",
        "Health": "fitness",

        "Cloud": "cloud",
        "AWS": "cloud",

        "News": "news",
        "Gaming": "gaming",
        "Food": "food"
    }

    return mapping.get(cat, "other")

class SubscriptionPipeline:

    def __init__(self):
        self.classifier = ClassifierAgent()
        self.extractor = ExtractorAgent()

    def run(self, transactions):
        results = []

        for txn in transactions:
            category = self.classifier.classify(txn["description"])
            result = self.extractor.extract(txn, category)
            results.append(result)

        return results


def send_to_m3(subscription):
    BASE_URL = "https://subscription-watchdog-m3-production.up.railway.app/mcp"

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream"
    }

    session = requests.Session()

    init_payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {
                "name": "m2-extraction-agent",
                "version": "1.0.0"
            }
        }
    }

    init_response = session.post(BASE_URL, headers=headers, json=init_payload, timeout=20)

    session_id = init_response.headers.get("mcp-session-id")
    print("SESSION ID:", session_id)

    headers["mcp-session-id"] = session_id

    add_sub_payload = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/call",
        "params": {
            "name": "add_sub",
            "arguments": {
                "merchant_name": subscription["merchant"],
                "raw_description": subscription["merchant"],
                "price": subscription["amount"],
                "currency": "USD",
                "billing_cycle": subscription["cycle"],
                "detected_date": "2026-06-22",
                "user_id": "user_42",
                "confidence": subscription["confidence"],
                "category": map_category(subscription["category"]),
                "is_recurring": True
            }
        }
    }

    response = session.post(BASE_URL, headers=headers, json=add_sub_payload, timeout=20)

    print("STATUS:", response.status_code)
    print("RESPONSE:", response.text)

    return response.text


def main():
    pipeline = SubscriptionPipeline()

    test_data = [
        {"description": "Netflix India", "amount": 499}
    ]

    results = pipeline.run(test_data)

    print("AI OUTPUT:", results)

    for item in results:
        response = send_to_m3(item)
        print("SENT TO M3:", response)


if __name__ == "__main__":
    main()