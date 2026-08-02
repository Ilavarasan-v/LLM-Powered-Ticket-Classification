# Day 4 Task - LLM Powered Ticket Classification 

# LLM-Powered Ticket Classification

An end-to-end NLP pipeline that classifies customer support tickets using Large Language Models (LLMs). The project predicts the ticket category, urgency, and customer sentiment while ensuring that every response follows a predefined JSON schema through validation and retry mechanisms.

This project was developed as part of a take-home assessment to demonstrate prompt engineering, structured LLM outputs, response validation, and evaluation across multiple prompting strategies.

---

## Features

- Classifies support tickets into predefined categories
- Predicts ticket urgency
- Identifies customer sentiment
- Supports multiple LLM providers with automatic failover
  - Groq
  - Google Gemini
  - OpenAI
- Implements both Zero-Shot and Few-Shot prompting
- Compares prompt strategies using a labeled validation dataset
- Validates every LLM response before accepting it
- Retries invalid responses automatically
- Falls back to default values if all providers fail
- Exports predictions to CSV and JSON
- Simple Streamlit interface for interactive testing

---

## Project Structure

```
day4_llm_ticket_classification/

├── data/
│   ├── support_tickets_raw.csv
│   └── support_tickets_validation_sample.csv
│
├── outputs/
│   ├── ticket_classifications.csv
│   ├── ticket_classifications.json
│   ├── zero_shot_predictions.csv
│   ├── few_shot_predictions.csv
│   └── prompt_strategy_comparison.csv
│
├── pipeline/
│   ├── app.py
│   ├── classifier.py
│   ├── evaluator.py
│   ├── final_classification.py
│   ├── prompt_comparison.py
│   ├── prompts.py
│   ├── providers.py
│   ├── utils.py
│   ├── validator.py
│   └── requirements.txt
│
├── CANDIDATE_TASK.md
├── LLM_REPORT.md
└── README.md
```

---

## Workflow

```
Support Ticket
      │
      ▼
Prompt Generation
      │
      ▼
Groq
      │
      ▼
Gemini
      │
      ▼
OpenAI
      │
      ▼
Response Validation
      │
      ▼
Output Normalization
      │
      ▼
Save Results
```

If one provider is unavailable due to quota limits or other errors, the pipeline automatically switches to the next provider before using fallback values.

---

## Prompt Engineering

Two prompting strategies were implemented and evaluated.

### 1. Zero-Shot Prompt

The model receives only instructions describing the task and the expected JSON output format.

### 2. Few-Shot Prompt

The model is provided with a few example tickets and their expected classifications before receiving the new ticket.

Both strategies were evaluated on the labeled validation dataset before selecting the final approach.

---

## Validation

Every model response goes through a validation pipeline before being accepted.

The validation checks include:

- Valid JSON format
- Required keys exist
- Category belongs to the allowed list
- Urgency belongs to the allowed list
- Sentiment belongs to the allowed list

If validation fails, the request is retried up to three times.

If all retries fail, the system returns a predefined fallback classification so the pipeline can continue processing.

---

## Prompt Strategy Comparison

The two prompting strategies were evaluated on the 14 labeled validation tickets.

| Strategy | Category | Urgency | Sentiment |
|----------|----------|----------|-----------|
| Zero-Shot | 71.43% | 71.43% | 71.43% |
| Few-Shot | 35.71% | 42.86% | 42.86% |

Based on these results, the Zero-Shot prompt was selected for classifying the complete dataset.

---

## Running the Project

### Install dependencies

```bash
pip install -r pipeline/requirements.txt
```

### Configure environment variables

Create a `.env` file with your API keys.

```
GROQ_API_KEY=your_key
GEMINI_API_KEY=your_key
OPENAI_API_KEY=your_key
```

### Run the complete classification pipeline

```bash
cd pipeline

python final_classification.py
```

### Compare prompt strategies

```bash
python prompt_comparison.py
```

### Launch the Streamlit application

```bash
streamlit run app.py
```

---

## Output Files

After execution the following files are generated.

- ticket_classifications.csv
- ticket_classifications.json
- zero_shot_predictions.csv
- few_shot_predictions.csv
- prompt_strategy_comparison.csv

---

## Technologies Used

- Python
- Pandas
- Streamlit
- Groq API
- Google Gemini API
- OpenAI API
- python-dotenv

---

## Notes

One challenge encountered during development was API quota limits while processing multiple tickets. To improve reliability, the pipeline was updated to support three providers with automatic failover. This allowed the classification process to continue even when one provider became unavailable.

Another observation was that the Zero-Shot prompt performed noticeably better than the Few-Shot prompt on the validation dataset. Although Few-Shot prompting often improves performance, the examples used in this task appeared to bias the model toward incorrect predictions for several validation tickets.

---

## Future Improvements

- Add confidence scores for predictions
- Support asynchronous batch processing
- Expose the pipeline as a REST API
- Add evaluation metrics such as precision, recall, and F1-score
- Store prediction history in a database
- Add support for additional LLM providers
