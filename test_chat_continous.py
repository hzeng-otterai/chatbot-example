import openai
from datetime import datetime

# Construct the system prompt
system_prompt_template = """You are Bobby, a virtual assistant create by Huajun. Today is {today}. You provide responses to questions that are clear, straightforward, and factually accurate, without speculation or falsehood. Given the following context, please answer each question truthfully to the best of your abilities based on the provided information. Answer each question with a brief summary followed by several bullet points. 

<context>
{context}
</context>
"""

with open("news_result.txt") as in_file:
  context_content = in_file.read()

system_prompt = system_prompt_template.format(
  context=context_content, 
  today=datetime.today().strftime('%Y-%m-%d')
)

history = []

# Loop to receive user input continously
while(True):
  user_input = input("> ")
  history.append({"role": "user", "content": user_input})

  llm_result = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "system", "content": system_prompt}] + history,
    stream=True,
  )

  # Receive tokens in streaming way
  buffer = ""
  for chunk in llm_result:
    next_token = chunk.choices[0].delta.get("content", "")
    print(next_token, flush=True, end="")
    buffer += next_token

  print()

  history.append({"role": "assistant", "content": buffer})

