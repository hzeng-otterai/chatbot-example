from openai import AsyncOpenAI
import time
import asyncio

client = AsyncOpenAI()

async def chat_func():
    result = await client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an AI assistant."},
            {"role": "user", "content": "Write an peom of python."},
        ],
        max_tokens=256,
        temperature=0.5,
        stream=True,
    )

    async for chunk in result:
        print(chunk.choices[0].delta.content, flush=True, end="")


asyncio.run(chat_func())