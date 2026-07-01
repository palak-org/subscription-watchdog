# statement_parser.py
# Parses bank statement CSV files and extracts subscriptions


import csv


def parse_statement(file_path):

    subscriptions = []

    try:
        with open(file_path, "r") as file:

            reader = csv.DictReader(file)

            for row in reader:

                subscription = {
                    "date": row["Date"],
                    "description": row["Description"],
                    "amount": float(row["Amount"]),
                    "type": row["Type"]
                }

                subscriptions.append(subscription)


        return subscriptions


    except Exception as e:
        print("Error while parsing statement:", e)
        return []