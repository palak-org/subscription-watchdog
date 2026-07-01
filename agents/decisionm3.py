def run_decision_engine(extracted, memory):

    alerts = []


    for sub in extracted:

        if sub["name"] not in memory:

            alerts.append(
                {
                    "type":"new",
                    "name":sub["name"],
                    "currency":sub["currency"],
                    "amount":sub["amount"]
                }
            )


    return alerts