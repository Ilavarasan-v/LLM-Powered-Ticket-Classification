# LLM Report

## Overview

The objective of this project was to build an LLM-powered pipeline capable of classifying customer support tickets into three fields:

- Category
- Urgency
- Sentiment

The pipeline was designed to produce structured JSON responses, validate every prediction before accepting it, and remain reliable even when an LLM provider became unavailable.

---

# Prompt Engineering

Two different prompting strategies were implemented and evaluated before selecting the final approach.

## Prompt Strategy 1 – Zero-Shot Prompt

The Zero-Shot prompt provides the model with task instructions, the list of allowed labels, and the required JSON format without showing any examples.

### Prompt

```text
You are a customer support ticket classifier.

Classify the following customer support ticket.

Allowed Categories:
- Billing
- Technical Issue
- Account Access
- Feature Request
- Complaint
- General Inquiry

Allowed Urgency:
- Low
- Medium
- High
- Critical

Allowed Sentiment:
- Positive
- Neutral
- Negative

Return ONLY valid JSON.

Example format:

{
  "category": "...",
  "urgency": "...",
  "sentiment": "..."
}

Ticket:
{ticket}
```

---

## Prompt Strategy 2 – Few-Shot Prompt

The Few-Shot prompt uses the same instructions but includes several worked examples before presenting the new ticket. The goal was to guide the model toward more consistent classifications.

### Prompt

```text
You are a customer support ticket classifier.

Example 1

Ticket:
"I was charged twice for my subscription."

Output:

{
  "category":"Billing",
  "urgency":"High",
  "sentiment":"Negative"
}

Example 2

Ticket:
"I forgot my password and cannot log in."

Output:

{
  "category":"Account Access",
  "urgency":"Medium",
  "sentiment":"Neutral"
}

Example 3

Ticket:
"The dashboard loads very slowly."

Output:

{
  "category":"Technical Issue",
  "urgency":"Medium",
  "sentiment":"Negative"
}

Now classify the following ticket.

Return ONLY valid JSON.

Ticket:
{ticket}
```

---

# Prompt Evaluation

Both prompt strategies were evaluated using the 14 labeled validation tickets.

The following accuracy was obtained.

| Prompt Strategy | Category Accuracy | Urgency Accuracy | Sentiment Accuracy |
|----------------|------------------:|-----------------:|-------------------:|
| Zero-Shot | **71.43%** | **71.43%** | **71.43%** |
| Few-Shot | 35.71% | 42.86% | 42.86% |

### Selected Strategy

The Zero-Shot prompt consistently outperformed the Few-Shot prompt across all three evaluation metrics. Although Few-Shot prompting often improves performance, the examples used in this project appeared to bias the model toward incorrect predictions for several validation tickets.

Based on these results, the Zero-Shot prompt was selected for classifying the complete dataset of 45 tickets.

---

# LLM Providers

To improve reliability, the project supports multiple LLM providers.

Provider order:

1. Groq
2. Google Gemini
3. OpenAI

Every request is first sent to Groq. If Groq is unavailable because of rate limits or other errors, the request automatically moves to Gemini. If Gemini also fails, the request is sent to OpenAI.

This approach allows the pipeline to continue processing without requiring manual intervention.

---

# Response Validation

Every response returned by the LLM is validated before it is accepted.

The validation process performs the following checks:

- Confirms the response is valid JSON.
- Confirms all required fields are present.
- Validates the category against the allowed labels.
- Validates the urgency against the allowed labels.
- Validates the sentiment against the allowed labels.

If validation fails, the request is retried up to three times.

If all retries fail, the pipeline assigns a default classification:

```json
{
    "category": "General Inquiry",
    "urgency": "Medium",
    "sentiment": "Neutral"
}
```

This prevents the entire pipeline from stopping because of a single invalid response.

---

# Output Generation

After validation, predictions are saved in both CSV and JSON formats.

Generated files:

- ticket_classifications.csv
- ticket_classifications.json
- zero_shot_predictions.csv
- few_shot_predictions.csv
- prompt_strategy_comparison.csv

---

# Observations

A few interesting observations came up while testing the pipeline.

The first was API quota limitations. During early testing, both Groq and Gemini exceeded their free-tier quotas while processing the dataset. To improve reliability, OpenAI was added as a third provider. This reduced interruptions and allowed the classification process to continue without changing the rest of the pipeline.

Another observation was that the Zero-Shot prompt produced more consistent predictions than the Few-Shot prompt. While Few-Shot prompting is commonly expected to improve performance, it performed noticeably worse on the validation dataset used in this project.

---

# Challenges

Some of the challenges encountered during development were:

- Ensuring every provider returned valid JSON.
- Handling malformed or incomplete model responses.
- Managing API rate limits across different providers.
- Keeping predictions consistent across multiple LLMs.
- Designing prompts that balanced accuracy with simplicity.

These issues were addressed through prompt refinement, response validation, retry logic, and provider failover.

---

# Conclusion

This project demonstrates a complete LLM-based text classification pipeline using prompt engineering, structured outputs, response validation, and multiple LLM providers.

The final pipeline successfully classified all support tickets while remaining resilient to provider failures and invalid model responses. The comparison between Zero-Shot and Few-Shot prompting also highlighted the importance of evaluating prompt strategies instead of assuming one approach will always perform better.
