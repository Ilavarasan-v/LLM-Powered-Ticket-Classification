import json
import pandas as pd
from providers import call_llm
from validator import clean_response, validate_response
from prompts import ZERO_SHOT_PROMPT, FEW_SHOT_PROMPT

VALIDATION_FILE = "../data/support_tickets_validation_sample.csv"


def classify_ticket(ticket_text, prompt_template):
    """
    Classify a ticket using the supplied prompt template.
    Retries up to 3 times before using fallback values.
    """

    for attempt in range(3):
        print(f"Attempt {attempt + 1}")

        prompt = prompt_template.format(ticket=ticket_text)

        response = call_llm(prompt)

        if not response:
            continue

        try:
            cleaned = clean_response(response)
            result = validate_response(cleaned)

            if result:
                return result

        except Exception:
            pass

    print("Using fallback values...")

    return {
        "category": "General Inquiry",
        "urgency": "Medium",
        "sentiment": "Neutral"
    }


def evaluate_prompt(prompt_name, prompt_template):
    print("=" * 70)
    print(f"Evaluating {prompt_name}")
    print("=" * 70)

    df = pd.read_csv(VALIDATION_FILE)

    predictions = []

    category_correct = 0
    urgency_correct = 0
    sentiment_correct = 0

    total = len(df)

    for _, row in df.iterrows():

        print(f"\nTicket : {row['ticket_id']}")

        prediction = classify_ticket(
            row["ticket_text"],
            prompt_template
        )

        predictions.append(prediction)

        if prediction["category"] == row["category"]:
            category_correct += 1

        if prediction["urgency"] == row["urgency"]:
            urgency_correct += 1

        if prediction["sentiment"] == row["sentiment"]:
            sentiment_correct += 1

    category_accuracy = (category_correct / total) * 100
    urgency_accuracy = (urgency_correct / total) * 100
    sentiment_accuracy = (sentiment_correct / total) * 100

    output = pd.DataFrame(predictions)

    output.insert(0, "ticket_id", df["ticket_id"])

    filename = f"../outputs/{prompt_name.lower().replace('-', '_')}_predictions.csv"

    output.to_csv(filename, index=False)

    print(f"\nSaved predictions -> {filename}")

    return {
        "Prompt Strategy": prompt_name,
        "Category Accuracy": round(category_accuracy, 2),
        "Urgency Accuracy": round(urgency_accuracy, 2),
        "Sentiment Accuracy": round(sentiment_accuracy, 2)
    }


def main():

    zero_results = evaluate_prompt(
        "Zero-Shot",
        ZERO_SHOT_PROMPT
    )

    few_results = evaluate_prompt(
        "Few-Shot",
        FEW_SHOT_PROMPT
    )

    comparison = pd.DataFrame([zero_results, few_results])

    print("\n")
    print("=" * 70)
    print("PROMPT COMPARISON")
    print("=" * 70)
    print(comparison.to_string(index=False))

    comparison.to_csv(
        "../outputs/prompt_strategy_comparison.csv",
        index=False
    )

    print("\nComparison saved to:")
    print("../outputs/prompt_strategy_comparison.csv")

    zero_score = (
        zero_results["Category Accuracy"]
        + zero_results["Urgency Accuracy"]
        + zero_results["Sentiment Accuracy"]
    )

    few_score = (
        few_results["Category Accuracy"]
        + few_results["Urgency Accuracy"]
        + few_results["Sentiment Accuracy"]
    )

    print("\n")
    print("=" * 70)

    if few_score > zero_score:
        print("Winning Strategy : FEW-SHOT")
    elif zero_score > few_score:
        print("Winning Strategy : ZERO-SHOT")
    else:
        print("Both strategies performed equally.")

    print("=" * 70)


if __name__ == "__main__":
    main()