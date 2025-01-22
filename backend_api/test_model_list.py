import json
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load the .env file
load_dotenv()

# Get the API key from the environment variable
api_key = os.getenv("OPENAI_API_KEY")

# Initialize the OpenAI client with the API key
client = OpenAI(api_key=api_key)

# List models
model_list = client.models.list()

print("Model list in object format.")
print(model_list)

print("Model list in dict format.")
print(model_list.to_dict())

print("Model list in JSON format.")
print(json.dumps(model_list.to_dict(), indent=2))