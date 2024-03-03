from openai import AsyncOpenAI
import time
import asyncio


async def chat_func():
    client = AsyncOpenAI()

    result = await client.chat.completions.create(
        messages=[
            {"role": "user", "content": "You are a puppy called Bummer."},
            {"role": "assistant", "content": "Woof!"},
            {"role": "user", "content": "Write a poem for me."},
        ],
        model="gpt-4",
        max_tokens=256,
        temperature=0.5,
        stream=True,
    )

    async for r in result:
        print(r.choices[0].delta.content, flush=True, end="")


asyncio.run(chat_func())