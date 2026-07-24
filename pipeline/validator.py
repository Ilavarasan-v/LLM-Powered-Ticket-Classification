"""
validator.py

Validates and cleans LLM outputs to enforce the required ticket schema.
"""

import json
import re

ALLOWED_CATEGORIES = {
    "Billing",
    "Technical Issue",
    "Account Access",
    "Feature Request",
    "Complaint",
    "General Inquiry",
}

ALLOWED_URGENCIES = {
    "Low",
    "Medium",
    "High",
    "Critical",
}

ALLOWED_SENTIMENTS = {
    "Positive",
    "Neutral",
    "Negative",
}


def clean_response(raw_response: str) -> dict:
    """
    Cleans raw LLM response text (removes markdown backticks, extra text)
    and parses it into a Python dictionary.
    """
    if not raw_response:
        raise ValueError("Empty response received from LLM.")

    text = raw_response.strip()

    # Remove markdown code block wrappers if present (e.g. ```json ... ```)
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
        text = re.sub(r"\s*```$", "", text)

    # Extract JSON object substring if model included extra text
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        text = match.group(0)

    try:
        data = json.loads(text)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse JSON response: {e}\nRaw output: {text}")

    return data


def validate_response(data: dict) -> dict:
    """
    Validates that parsed JSON contains required fields and all values match allowed enums.
    """
    if not isinstance(data, dict):
        raise ValueError(f"Expected JSON object, got {type(data).__name__}")

    required_fields = ["category", "urgency", "sentiment"]
    for field in required_fields:
        if field not in data:
            raise ValueError(f"Missing required field: '{field}'")

    category = data["category"]
    urgency = data["urgency"]
    sentiment = data["sentiment"]

    if category not in ALLOWED_CATEGORIES:
        raise ValueError(f"Invalid category '{category}'. Allowed: {ALLOWED_CATEGORIES}")

    if urgency not in ALLOWED_URGENCIES:
        raise ValueError(f"Invalid urgency '{urgency}'. Allowed: {ALLOWED_URGENCIES}")

    if sentiment not in ALLOWED_SENTIMENTS:
        raise ValueError(f"Invalid sentiment '{sentiment}'. Allowed: {ALLOWED_SENTIMENTS}")

    return {
        "category": category,
        "urgency": urgency,
        "sentiment": sentiment,
    }
