import google.generativeai as genai
import os
import re

# Load your Gemini API key from environment variable
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise RuntimeError("GOOGLE_API_KEY environment variable not set")

genai.configure(api_key=api_key)

def extract_fields(response_text):
    intent = re.search(r"Intent:\s*(.*)", response_text)
    leave_type = re.search(r"Leave Type:\s*(.*)", response_text)
    start_date = re.search(r"Start Date:\s*(.*)", response_text)
    num_days = re.search(r"Number of Days:\s*(.*)", response_text)

    # Try parsing num_days only if it's a valid number
    num_days_value = None
    if num_days:
        try:
            num_days_value = int(num_days.group(1).strip())
        except ValueError:
            num_days_value = None

    return {
        "intent": intent.group(1).strip() if intent else None,
        "leave_type": leave_type.group(1).strip() if leave_type else None,
        "start_date": start_date.group(1).strip() if start_date else None,
        "num_days": num_days_value,
    }


def process_user_input(user_input):
    system_message = (
        "You are an HR assistant for a Leave Management System. "
        "Extract the user's intent and all necessary fields. "
        "Only reply using this exact format:\n"
        "Intent: <intent>\n"
        "Leave Type: <leave type>\n"
        "Start Date: <YYYY-MM-DD or None>\n"
        "Number of Days: <integer or None>\n"
        "Valid intents are: check_balance, request_leave, cancel_leave, view_history"
    )

    # Use a valid model name
    chat = genai.GenerativeModel('models/gemini-1.5-flash').start_chat()

    response = chat.send_message(f"{system_message}\n\n{user_input}")

    return extract_fields(response.text)
