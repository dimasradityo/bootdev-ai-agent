import argparse
import os

from dotenv import load_dotenv
from openai import OpenAI


def main():
    # configuring env vars and assigning api key
    load_dotenv()
    api_key: str | None = os.environ.get("OPENROUTER_API_KEY")
    if api_key is None:
        raise RuntimeError("API key not found.")

    # create OpenAI client
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    # Create Arg Parser object
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    # create new chat
    messages: list[dict[str, str]] = [
        {"role": "user", "content": args.user_prompt},
    ]

    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
    )

    # display output
    usage: object = response.usage
    if usage is None:
        raise RuntimeError(
            "No usage data to display. Check if API request was successful."
        )

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {usage.prompt_tokens}")
        print(f"Response tokens: {usage.completion_tokens}")
    print(f"Response: {response.choices[0].message.content}")


if __name__ == "__main__":
    main()
