"""Build an AI-Agent - Boot.dev project."""

import argparse
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
API_KEY = os.environ.get("GEMINI_API_KEY")


# --------------------------------------------------
def main() -> None:
    """Make a jazz noise here."""
    args = get_args()
    user_prompt = " ".join(args.prompt)

    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]
    client = genai.Client(api_key=API_KEY)

    if args.verbose:
        print(f"Working on: {user_prompt}\n")

    generate_content(client, messages, verbose=args.verbose)


# --------------------------------------------------
def get_args() -> argparse.Namespace:
    """Get command-line arguments.

    Returns:
        Parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(
        description="AI Coding Agent",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument("prompt", help="Prompt for LLM", metavar="prompt", type=str, nargs="+")
    parser.add_argument("-v", "--verbose", help="Flag to include additional information", action="store_true")

    return parser.parse_args()

    # this is here to try to try to force an exit code of 1 to match the tests
    # try:
    #     args = parser.parse_args()
    # except argparse.ArgumentError:
    #     print("must provide a prompt")
    #     sys.exit(1)
    # else:
    #     return args


# --------------------------------------------------
def generate_content(client: genai.Client, messages: list[types.Content], *, verbose: bool) -> None:
    """Generate content from the LLM and prints it to the terminal.

    Args:
        client: The AI Client.
        messages: List of all messages in the conversation.
        verbose: Print additional information if true.
    """
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
    )
    print("Response:")
    print(response.text)

    if verbose:
        prompt_token_count: int | None = 0
        response_token_count: int | None = 0
        if response.usage_metadata:
            prompt_token_count = response.usage_metadata.prompt_token_count
            response_token_count = response.usage_metadata.candidates_token_count

        print(f"Prompt tokens: {prompt_token_count}")
        print(f"Response tokens: {response_token_count}")


if __name__ == "__main__":
    main()
