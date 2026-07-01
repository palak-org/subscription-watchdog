

import re

def extract_subscriptions(text):

    subscriptions = []

    keywords = ["NETFLIX", "SPOTIFY", "AMAZON PRIME"]

    for line in text.split(","):   # IMPORTANT: split by comma input

        for key in keywords:

            if key.lower() in line.lower():

                match = re.search(r'(\d+(\.\d+)?)', line)

                if match:
                    amount = float(match.group(1))
                else:
                    amount = 0

                subscriptions.append({
                    "name": key,
                    "amount": amount,
                    "currency": "₹"
                })

    return subscriptions