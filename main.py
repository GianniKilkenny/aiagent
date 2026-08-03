import argparse
import os
from prompts import system_prompt
from dotenv import load_dotenv
from openai import OpenAI
import json
from call_function import available_functions, call_function
import sys

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
    for _ in range(20):
        response = client.chat.completions.create(
            model= "openrouter/free",
            messages = messages,
            tools= available_functions,
        )
        if response.usage is None:
            raise RuntimeError("There is an error with the API's response usage")

        message = response.choices[0].message
        messages.append(message)
        if verbose:
            print("Prompt tokens:", response.usage.prompt_tokens)
            print("Response tokens:", response.usage.completion_tokens)

        if not message.tool_calls:
            print("Response:")
            print(message.content)
            return

        for tool_call in message.tool_calls:
            result_message = call_function(tool_call, verbose)
            if not result_message.get('content'):
                raise RuntimeError(f"Empty function response for {tool_call.function.name}")
            messages.append(result_message)
            if verbose:
                print(f"-> {result_message['content']}")

    print("We were not able to come up with a final answer within 20 iterations")
    sys.exit(1)


if __name__ == "__main__":
    main()

