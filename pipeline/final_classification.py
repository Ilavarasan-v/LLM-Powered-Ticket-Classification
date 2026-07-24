"""
final_classification.py

Reads all tickets, classifies them using the LLM,
and saves the results as CSV and JSON.
"""

import json
import pandas as pd

from classifier import classify_ticket

# -----------------------------
# File Paths
# -----------------------------

import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INPUT_FILE = os.path.join(BASE_DIR, "data", "support_tickets_raw.csv")
CSV_OUTPUT = os.path.join(BASE_DIR, "outputs", "ticket_classifications.csv")
JSON_OUTPUT = os.path.join(BASE_DIR, "outputs", "ticket_classifications.json")

# -----------------------------
# Load Dataset
# -----------------------------

df = pd.read_csv(INPUT_FILE)

print("=" * 70)
print(f"Loaded {len(df)} Tickets")
print("=" * 70)

results = []

# -----------------------------
# Classify Tickets
# -----------------------------

for index, row in df.iterrows():

    ticket_id = row["ticket_id"]
    ticket_text = row["ticket_text"]

    print(f"\nProcessing {ticket_id} ({index + 1}/{len(df)})")

    prediction = classify_ticket(ticket_id, ticket_text)

    results.append({

        "ticket_id": ticket_id,

        "ticket_text": ticket_text,

        "category": prediction["category"],

        "urgency": prediction["urgency"],

        "sentiment": prediction["sentiment"]

    })

# -----------------------------
# Save CSV
# -----------------------------

results_df = pd.DataFrame(results)

results_df.to_csv(

    CSV_OUTPUT,

    index=False

)

print(f"\nCSV Saved -> {CSV_OUTPUT}")

# -----------------------------
# Save JSON
# -----------------------------

with open(

    JSON_OUTPUT,

    "w",

    encoding="utf-8"

) as f:

    json.dump(

        results,

        f,

        indent=4,

        ensure_ascii=False

    )

print(f"JSON Saved -> {JSON_OUTPUT}")

# -----------------------------
# Summary
# -----------------------------

print("\n")
print("=" * 70)
print("Classification Completed")
print("=" * 70)

print(f"Total Tickets : {len(results_df)}")

print("\nCategory Distribution")
print(results_df["category"].value_counts())

print("\nUrgency Distribution")
print(results_df["urgency"].value_counts())

print("\nSentiment Distribution")
print(results_df["sentiment"].value_counts())