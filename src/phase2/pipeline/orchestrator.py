from src.phase2.agents.classifier_agent import ClassifierAgent
from src.phase2.agents.extractor_agent import ExtractorAgent


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


def main():
    pipeline = SubscriptionPipeline()

    test_data = [
        {"description": "Netflix India", "amount": 499}
    ]

    print(pipeline.run(test_data))


if __name__ == "__main__":
    main()