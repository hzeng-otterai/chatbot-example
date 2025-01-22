from openai import OpenAI
from dotenv import load_dotenv
import os

# Load the .env file
load_dotenv()

# Get the API key from the environment variable
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

result = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "system", 
            "content": "You are a helpful assistant."
        },
        {
            "role": "user",
            "content": "Write a poem about recursion in programming."
        }
    ]
)

print(result)

print(result.choices[0].message)

print(result.choices[0].message.content)
