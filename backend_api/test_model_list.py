import json
from openai import OpenAI
client = OpenAI()

model_list = client.models.list()

print("Model list in object format.")
print(model_list)

print("Model list in dict format.")
print(model_list.to_dict())

print("Model list in JSON format.")
print(json.dumps(model_list.to_dict(), indent=2))