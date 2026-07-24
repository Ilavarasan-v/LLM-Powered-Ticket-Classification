"""
classifier.py

Main ticket classification pipeline.

Flow:

Ticket
    ↓
Prompt
    ↓
Groq
    ↓
Gemini (Fallback)
    ↓
Validation
    ↓
Retry
    ↓
Fallback Labels
"""

from providers import call_llm
from validator import clean_response, validate_response
from prompts import ZERO_SHOT_PROMPT
from utils import log_invalid_response

MAX_RETRIES = 3


def build_prompt(ticket_text):
    """
    Build the prompt by inserting the ticket text.
    """
    return ZERO_SHOT_PROMPT.format(ticket=ticket_text)


def classify_ticket(ticket_id, ticket_text):
    """
    Classify a single support ticket.

    Parameters
    ----------
    ticket_id : str
    ticket_text : str

    Returns
    -------
    dict
    """

    prompt = build_prompt(ticket_text)

    last_response = None
    last_error = None

    for attempt in range(1, MAX_RETRIES + 1):

        print("=" * 60)
        print(f"{ticket_id} | Attempt {attempt}")
        print("=" * 60)

        response = call_llm(prompt)

        if response is None:

            print("No response from provider.")

            continue

        last_response = response

        try:

            cleaned = clean_response(response)

            validated = validate_response(cleaned)

            print("✅ Classification Successful\n")

            return validated

        except Exception as e:

            last_error = e

            print(f"❌ Validation Failed : {e}")

            log_invalid_response(
                ticket_id=ticket_id,
                response=response,
                error=e
            )

            print("Retrying...\n")

    print("=" * 60)
    print("Maximum retries reached.")
    print("Using fallback values.")
    print("=" * 60)

    return {

        "category": "General Inquiry",

        "urgency": "Medium",

        "sentiment": "Neutral"

    }