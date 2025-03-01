import json

import re
import json

def extract_json_with_data(text):
    try:
        # Match JSON-like structure that contains the "data" key
        json_match = re.search(r'\{.*?"data"\s*:\s*\[.*?\].*?\}', text, re.S)
        if json_match:
            json_str = json_match.group(0)
            data = json.loads(json_str)
            
            # Ensure "data" key exists and is a list
            if "data" in data and isinstance(data["data"], list):
                return data
        print("No valid JSON with 'data' key found.")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return None



def format_ai_response(response):
    """
    Formats the AI JSON response into a human-readable string.

    Args:
        response (str or dict): AI response in JSON format (string or dictionary).

    Returns:
        str: Formatted output.
    """
    # Ensure response is a dictionary (parse if it's a JSON string)
    if isinstance(response, str):
        try:
            response = json.loads(response)
        except json.JSONDecodeError:
            return response

    # Validate the 'data' key exists
    if 'data' not in response or not isinstance(response['data'], list):
        return "Invalid response structure. Missing 'data' key."

    answers = response['data']

    # Handle cases where there is no data
    if not answers:
        return "No answers available."

    # Format output based on the number of answers
    if len(answers) == 1:
        return f"1. {answers[0]}"
    else:
        return "\n".join([f"{i + 1}. {answer}" for i, answer in enumerate(answers)])
