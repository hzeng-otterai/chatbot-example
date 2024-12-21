from openai import AsyncOpenAI
import time
import asyncio

system_prompt_template = """You are {name} a virtual assistant created by {owner}. Today is {date}. You provide responses to questions that are clear, straightforward, and factually accurate, without speculation or falsehood. Given the following context, please answer each question truthfully to the best of your abilities based on the provided information. Answer each question with a brief summary followed by several bullet points. 

Example:
Summary of answer
- bullet point 1
- bullet point 2
...

<context>
{context}
</context>
"""

with open("news_result.txt") as in_file:
    context_content = in_file.read()

system_prompt = system_prompt_template.format(
    name="Robot",
    owner="Huajun",
    date="Dec. 20th, 2024",
    context=context_content
)

async def chat_func():
    client = AsyncOpenAI()

    result = await client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": "Any news about cell phones?"}
        ],
        max_tokens=256,
        temperature=0.5,
        stream=True,
    )

    #print(result.choices[0].message.content)
    async for token in result:
        print(token.choices[0].delta.content, flush=True, end="")


asyncio.run(chat_func())