from openai import OpenAI

def call_openai():
    client = OpenAI()

    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "user", "content": "You are a puppy called Bummer."},
            {"role": "assistant", "content": "Woof!"},
            {"role": "user", "content": "What's your name?"},
        ],
        model="gpt-4",
    )

    return chat_completion.choices[0].message.content

print(call_openai())