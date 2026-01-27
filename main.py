import os
from dotenv import load_dotenv
from google import genai
import argparse


def main():
    parser = argparse.ArgumentParser(description="AI_Agent")
    parser.add_argument("user_prompt", type=str, help="Type your questions")
    args = parser.parse_args()
    
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY env variable is not set")

    
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model = "gemini-2.5-flash",
        contents = args.user_prompt
    )

    # "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."

    if not response.usage_metadata:
        raise RuntimeError("usage_metadata not available")

    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count
    print(f"Prompt tokens:{prompt_tokens}")
    print(f"Response tokens:{response_tokens}")
    print(f"Response: {response.text}")


if __name__ == "__main__":
    main()
