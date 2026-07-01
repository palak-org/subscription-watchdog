# orchestrator.py

from agents.extractor1 import extract_subscriptions


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


    def run(self, transactions):

        # Convert transactions into text
        text = str(transactions)


        # Extract subscriptions
        results = extract_subscriptions(text)


        # Add category
        for item in results:

            if "category" in item:

                item["category"] = map_category(
                    item["category"]
                )


        return results