class ExtractorAgent:
    def extract(self, transaction: dict, category: str):

        description = transaction["description"]

        cycle = "monthly"
        if "year" in description.lower():
            cycle = "yearly"

        return {
            "merchant": description.split()[0],
            "category": category,
            "amount": float(transaction["amount"]),
            "cycle": cycle,
            "confidence": 0.90
        }