import argparse
import json
from pathlib import Path
from typing import Optional
from cli import __version__
from ai.providers.openai import get_ai_client

CONFIG_PATH = Path.home() / ".askai" / "config.json"

def save_api_key(api_key: str):
    """Save the API key."""
    CONFIG_PATH.parent.mkdir(exist_ok=True)
    with open(CONFIG_PATH, "w") as f:
        json.dump({"OPENROUTER_API_KEY": api_key}, f)
    print(f"✅ API key saved to {CONFIG_PATH}")

def get_api_key() -> Optional[str]:
    """Retrieve the saved API key."""
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, "r") as f:
            return json.load(f).get("OPENROUTER_API_KEY")
    return None

def ask_question(question: str):
    """Ask the AI a question."""
    api_key = get_api_key()
    if not api_key:
        print("❌ Error: API key not set. Use 'askai set-api-key <YOUR_API_KEY>' to set it.")
        return

    ai_client = get_ai_client(provider="openrouter", api_key=api_key)
    answer = ai_client.ask(question)
    print(f"🤖 AI \n{answer}")

def main():
    try:
        parser = argparse.ArgumentParser(prog="askai", description="Ask AI anything!")
        parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}')
        
        # Create subparsers for structured commands
        subparsers = parser.add_subparsers(dest="command")

        # "question" subcommand (optional for explicit use)
        question_parser = subparsers.add_parser("question", help="Ask the AI a question.")
        question_parser.add_argument("question", type=str, help="Your question.")

        # "set-api-key" subcommand
        api_key_parser = subparsers.add_parser("set-api-key", help="Set your OpenRouter API key.")
        api_key_parser.add_argument("key", type=str, help="Your OpenRouter API key.")


        # Parse arguments
        args = parser.parse_args()

        # Logic to handle different cases
        if args.command == "set-api-key":
            save_api_key(args.key)
        elif args.command == "question":
            ask_question(args.question)
        elif args.input:  # Handle direct question
            ask_question(args.input)
        else:
            parser.print_help()
    except Exception as e:
        print(f"Error: {e}")
        print("Error: Something went wrong. Please try again.")
