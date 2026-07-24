"""
prompts.py

Contains all prompt templates used for ticket classification.
"""

# ==========================================================
# Zero-Shot Prompt
# ==========================================================

ZERO_SHOT_PROMPT = """
You are an expert AI customer support ticket classifier.

Your task is to analyze the support ticket and classify it into exactly one value for each field.

Categories:
- Billing
- Technical Issue
- Account Access
- Feature Request
- Complaint
- General Inquiry

Urgency:
- Low
- Medium
- High
- Critical

Sentiment:
- Positive
- Neutral
- Negative

Support Ticket:
{ticket}

Return ONLY valid JSON.

Example:

{{
    "category": "Technical Issue",
    "urgency": "High",
    "sentiment": "Negative"
}}

Do not explain anything.
Do not use markdown.
Return only JSON.
"""

# ==========================================================
# Few-Shot Prompt
# ==========================================================

FEW_SHOT_PROMPT = """
You are an expert AI customer support ticket classifier.

Below are examples.

Example 1

Ticket:
"I was charged twice for my subscription."

Output:

{{
    "category":"Billing",
    "urgency":"High",
    "sentiment":"Negative"
}}

----------------------------------------

Example 2

Ticket:
"I forgot my password and cannot login."

Output:

{{
    "category":"Account Access",
    "urgency":"High",
    "sentiment":"Negative"
}}

----------------------------------------

Example 3

Ticket:
"It would be nice if you add dark mode."

Output:

{{
    "category":"Feature Request",
    "urgency":"Low",
    "sentiment":"Neutral"
}}

----------------------------------------

Example 4

Ticket:
"The application crashes every time I upload a file."

Output:

{{
    "category":"Technical Issue",
    "urgency":"Critical",
    "sentiment":"Negative"
}}

----------------------------------------

Example 5

Ticket:
"Your support team never responds to my emails."

Output:

{{
    "category":"Complaint",
    "urgency":"Medium",
    "sentiment":"Negative"
}}

----------------------------------------

Now classify the following ticket.

Ticket:

{ticket}

Return ONLY valid JSON.

{{
    "category":"...",
    "urgency":"...",
    "sentiment":"..."
}}

Do not explain.
Do not use markdown.
Return only JSON.
"""