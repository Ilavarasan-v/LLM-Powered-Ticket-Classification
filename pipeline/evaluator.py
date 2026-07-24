"""
evaluator.py

Evaluates the classification results against the
ground truth labels.

Metrics:
- Category Accuracy
- Urgency Accuracy
- Sentiment Accuracy
"""

import pandas as pd
from sklearn.metrics import accuracy_score, classification_report


# ----------------------------------------------------
# File Paths
# ----------------------------------------------------

import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

GROUND_TRUTH_FILE = os.path.join(BASE_DIR, "data", "support_tickets_validation_sample.csv")
PREDICTIONS_FILE = os.path.join(BASE_DIR, "outputs", "ticket_classifications.csv")


# ----------------------------------------------------
# Load Data
# ----------------------------------------------------

ground_truth = pd.read_csv(GROUND_TRUTH_FILE)

predictions = pd.read_csv(PREDICTIONS_FILE)


# ----------------------------------------------------
# Merge Data
# ----------------------------------------------------

df = ground_truth.merge(
    predictions,
    on="ticket_id",
    suffixes=("_true", "_pred")
)


# ----------------------------------------------------
# Category Accuracy
# ----------------------------------------------------

category_accuracy = accuracy_score(
    df["category_true"],
    df["category_pred"]
)

print("=" * 60)
print("CATEGORY")
print("=" * 60)

print(f"Accuracy : {category_accuracy:.2%}")

print(
    classification_report(
        df["category_true"],
        df["category_pred"]
    )
)


# ----------------------------------------------------
# Urgency Accuracy
# ----------------------------------------------------

urgency_accuracy = accuracy_score(
    df["urgency_true"],
    df["urgency_pred"]
)

print("=" * 60)
print("URGENCY")
print("=" * 60)

print(f"Accuracy : {urgency_accuracy:.2%}")

print(
    classification_report(
        df["urgency_true"],
        df["urgency_pred"]
    )
)


# ----------------------------------------------------
# Sentiment Accuracy
# ----------------------------------------------------

sentiment_accuracy = accuracy_score(
    df["sentiment_true"],
    df["sentiment_pred"]
)

print("=" * 60)
print("SENTIMENT")
print("=" * 60)

print(f"Accuracy : {sentiment_accuracy:.2%}")

print(
    classification_report(
        df["sentiment_true"],
        df["sentiment_pred"]
    )
)


# ----------------------------------------------------
# Overall Summary
# ----------------------------------------------------

print("\n")
print("=" * 60)
print("FINAL RESULTS")
print("=" * 60)

print(f"Category Accuracy  : {category_accuracy:.2%}")
print(f"Urgency Accuracy   : {urgency_accuracy:.2%}")
print(f"Sentiment Accuracy : {sentiment_accuracy:.2%}")