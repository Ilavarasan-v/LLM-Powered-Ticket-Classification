"""
providers.py

Handles communication with multiple LLM providers.

Provider Order:
1. Groq (Primary)
2. Gemini (Secondary)
3. OpenAI (Final Provider)

If Groq fails (rate limit, timeout, etc.),
Gemini is automatically used.

If Gemini also fails,
OpenAI is used.

If all providers fail,
None is returned and the classifier
will use fallback values.
"""

import os
import time

from dotenv import load_dotenv
from groq import Groq
import google.generativeai as genai
from openai import OpenAI

# ---------------------------------------------------
# Load Environment Variables
# ---------------------------------------------------

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# ---------------------------------------------------
# Initialize Clients
# ---------------------------------------------------

groq_client = None
gemini_model = None
openai_client = None

if GROQ_API_KEY:
    groq_client = Groq(api_key=GROQ_API_KEY)

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    gemini_model = genai.GenerativeModel("gemini-2.5-flash")

if OPENAI_API_KEY:
    openai_client = OpenAI(api_key=OPENAI_API_KEY)

# ---------------------------------------------------
# Groq Provider
# ---------------------------------------------------

def call_groq(prompt: str):

    if groq_client is None:
        print("Groq API Key not found.")
        return None

    try:

        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",

            messages=[
                {
                    "role": "system",
                    "content":
                    (
                        "You are a customer support ticket classifier.\n"
                        "Return ONLY valid JSON.\n"
                        "Do not include markdown."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0,

            response_format={
                "type": "json_object"
            }
        )

        print("✓ Response from Groq")

        return response.choices[0].message.content

    except Exception as e:

        print(f"Groq Error : {e}")

        return None


# ---------------------------------------------------
# Gemini Provider
# ---------------------------------------------------

def call_gemini(prompt: str):

    if gemini_model is None:
        print("Gemini API Key not found.")
        return None

    try:

        response = gemini_model.generate_content(

            prompt,

            generation_config={
                "temperature": 0,
                "response_mime_type": "application/json"
            }

        )

        print("✓ Response from Gemini")

        return response.text

    except Exception as e:

        print(f"Gemini Error : {e}")

        return None


# ---------------------------------------------------
# OpenAI Provider
# ---------------------------------------------------

def call_openai(prompt: str):

    if openai_client is None:
        print("OpenAI API Key not found.")
        return None

    try:

        response = openai_client.chat.completions.create(

            # Change this model if you're using another one
            model="gpt-4.1-mini",

            messages=[
                {
                    "role": "system",
                    "content":
                    (
                        "You are a customer support ticket classifier.\n"
                        "Return ONLY valid JSON.\n"
                        "Do not include markdown."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0,

            response_format={
                "type": "json_object"
            }

        )

        print("✓ Response from OpenAI")

        return response.choices[0].message.content

    except Exception as e:

        print(f"OpenAI Error : {e}")

        return None


# ---------------------------------------------------
# Main Provider
# ---------------------------------------------------

def call_llm(prompt: str):

    # Try Groq
    print("\nTrying Groq...")

    response = call_groq(prompt)

    if response:
        return response

    time.sleep(1)

    # Try Gemini
    print("\nSwitching to Gemini...")

    response = call_gemini(prompt)

    if response:
        return response

    time.sleep(1)

    # Try OpenAI
    print("\nSwitching to OpenAI...")

    response = call_openai(prompt)

    if response:
        return response

    print("\nAll LLM providers failed.")

    return None