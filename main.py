import os
from dotenv import load_dotenv
from openai import OpenAI




load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")
if api_key is None:
    raise RuntimeError("OPENROUTER_API_KEY not set in .env")
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

api_key = os.environ.get("OPENROUTER_API_KEY")

def main():
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=[
            {
                "role": "user",
                "content": "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.",
            }
        ],
    )
    if response.usage is None:
        raise RuntimeError("There is an error with the API's response usage")
    print(f"Prompt tokens: {response.usage.prompt_tokens}")
    print(f"Response tokens: {response.usage.completion_tokens}")
    print("Response:")
    print(response.choices[0].message.content)


if __name__ == "__main__":
    main()

