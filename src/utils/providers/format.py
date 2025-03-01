import json

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
            return "Invalid response format."

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
