from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
import json

from ui.input_handler import get_user_input       # Member 1
from agents.extractorm1 import extract_subscriptions   # Member 2
from agents.memorym2 import load_memory, save_memory   # Member 3
from agents.decisionm3 import run_decision_engine      # Member 4
from agents.statement_parser import parse_statement  # Statement parser


def run_watchdog(raw_text=None):

    print("\n====================================")
    print("    SUBSCRIPTION WATCHDOG AGENT")
    print("====================================\n")


    # STEP 1: Get raw input

    print("Step 1: Getting your subscription data...\n")


    if raw_text is None:
        raw_text = get_user_input()


    if not raw_text.strip():

        print("No input received. Please paste your statement.")
        return


    # ── STEP 1.5: Parse uploaded statement file ──────────────

    print("\nParsing statement file...\n")

    file_path = "data/sample_statement.csv"

    parsed_data = parse_statement(file_path)


    print("Parsed Statement:")

    for item in parsed_data:

        print(item)



    # ── STEP 2: Extract subscriptions ─────────────────────────

    print("\nStep 2: Extracting subscriptions from your data...\n")


    extracted = extract_subscriptions(raw_text)


    if not extracted:

        print("Could not find any subscriptions in the text. Try again.")
        return



    print(f"  Found {len(extracted)} subscription(s):")


    for sub in extracted:

        print(f"    → {sub['name']} : {sub['currency']} {sub['amount']}")



    # ── STEP 3: Load memory and compare ──────────────────────

    print("\nStep 3: Comparing with your subscription history...\n")


    memory = load_memory()



    # ── STEP 4: Decision engine ───────────────────────────────

    print("Step 4: Analysing for price changes and unused subscriptions...\n")


    alerts = run_decision_engine(extracted, memory)



    # ── STEP 5: Show results ─────────────────────────────────

    print("\n====================================")
    print("          WATCHDOG REPORT")
    print("====================================\n")



    if not alerts:

        print("✅ All clear! No changes or issues detected.\n")


    else:

        for alert in alerts:


            if alert["type"] == "new":

                print(
                    f"🆕 NEW SUBSCRIPTION DETECTED: "
                    f"{alert['name']} — {alert['currency']} {alert['amount']}/month"
                )



            elif alert["type"] == "price_increase":

                print(f"📈 PRICE INCREASE: {alert['name']}")

                print(
                    f"   Was: {alert['currency']} {alert['old']} "
                    f"→ Now: {alert['currency']} {alert['new']}"
                )



            elif alert["type"] == "possible_cancel":

                print(f"⚠️ UNUSED SUBSCRIPTION: {alert['name']}")

                print(
                    f"   You haven't used this in "
                    f"{alert['days_unused']} days."
                )

                print(
                    "   Draft cancellation email? "
                    "Type YES to generate one.\n"
                )


                user_choice = input("   Your choice: ").strip().upper()


                if user_choice == "YES":

                    from agents.decision import draft_cancellation_email

                    email = draft_cancellation_email(alert["name"])

                    print(
                        f"\n--- CANCELLATION EMAIL DRAFT ---\n"
                        f"{email}\n"
                    )


            print()



    # ── STEP 5b: Update memory ────────────────────────────────

    save_memory(extracted)


    print("Memory updated. Your watchdog will remember this scan.")

    print("\n====================================\n")
    return alerts

    # ── UI Function ───────────────────────────────────────────────

def run_project(statement):

    return run_watchdog(statement)



# ── Entry point ───────────────────────────────────────────────

if __name__ == "__main__":

    run_watchdog()
