from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

from langchain_core.messages import HumanMessage, SystemMessage


llm1 = ChatOpenAI()
llm2 = ChatAnthropic(model_name="claude-2.0")

messages = [
    SystemMessage(content="You're a helpful assistant"),
    HumanMessage(content="Suggest some good names for a shoe company."),
]

result1 = llm1.invoke(messages)
print("Result from OpenAI:", result1.content)

result2 = llm2.invoke(messages)
print("Result from Anthropic:", result2.content)

print("Streaming result from OpenAI:")
for chunk in llm1.stream(messages):
    print(chunk.content, end="", flush=True)
print("\n")

print("Streaming result from Anthropic:")
for chunk in llm2.stream(messages):
    print(chunk.content, end="", flush=True)
print("\n")
