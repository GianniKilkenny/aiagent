import argparse
import os
from prompts import system_prompt
from dotenv import load_dotenv
from openai import OpenAI


def main():
    parser = argparse.ArgumentParser(description = "aiagent")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable Verbose Output")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if api_key is None:
        raise RuntimeError("OPENROUTER_API_KEY not set in .env")
    
    
    client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
    )
    

    messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": args.user_prompt,}
        ]
    
    if args.verbose:
        print(f"User prompt: {args.user_prompt}\n")
    
    generate_content(client, messages, args.verbose)

def generate_content(client: OpenAI, messages:list, verbose: bool):
    response = client.chat.completions.create(
        model= "openrouter/free",
        messages = messages,
        temperature=0
    )
    if response.usage is None:
        raise RuntimeError("There is an error with the API's response usage")
    if verbose:
        print("Prompt tokens:", response.usage.prompt_tokens)
        print("Response tokens:", response.usage.completion_tokens)
    print("Response:")
    print(response.choices[0].message.content)


if __name__ == "__main__":
    main()

