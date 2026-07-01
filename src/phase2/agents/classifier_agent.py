class ClassifierAgent:
    def classify(self, description: str):
        description = description.lower()

        if "netflix" in description:
            return "Entertainment"
        if "spotify" in description:
            return "Entertainment"
        if "amazon" in description:
            return "Shopping"
        if "uber" in description:
            return "Transport"

        return "Unknown"