import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse


def main():
    parser = argparse.ArgumentParser(description="AI_Agent")
    parser.add_argument("user_prompt", type=str, help="Prompt for Gemini")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY env variable is not set")

    client = genai.Client(api_key=api_key)
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    response = client.models.generate_content(
        model = "gemini-2.5-flash",
        contents = messages
    )

    # "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."

    if not response.usage_metadata:
        raise RuntimeError("usage_metadata not available")

    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens:{prompt_tokens}")
        print(f"Response tokens:{response_tokens}")
    else:
        print(f"Response: {response.text}")


if __name__ == "__main__":
    main()
