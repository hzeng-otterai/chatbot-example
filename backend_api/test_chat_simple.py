from openai import OpenAI
client = OpenAI()

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
