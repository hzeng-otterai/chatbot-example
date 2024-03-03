from openai import AsyncOpenAI
import time
import asyncio


async def chat_func():
    client = AsyncOpenAI()

    result = await client.chat.completions.create(
        messages=[
            {"role": "user", "content": "You are a puppy called Bummer."},
            {"role": "assistant", "content": "Woof!"},
            {"role": "user", "content": "What's your name?"},
        ],
        model="gpt-4",
        max_tokens=256,
        temperature=0.5,
    )

    print(result.choices[0].message.content)

# cannot do
# chat_func()

asyncio.run(chat_func())