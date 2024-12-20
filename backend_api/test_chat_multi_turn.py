from openai import OpenAI
client = OpenAI()

def call_openai():

    result = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an AI assistant."},
            {"role": "user", "content": "Who is the US president in 2000?"},
            {"role": "assistant", "content": "Bill Clinton"},
            {"role": "user", "content": "Who comes after him?"},
        ],
    )

    return result.choices[0].message.content

print(call_openai())
