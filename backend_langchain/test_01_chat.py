from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

llm1 = ChatOpenAI()
llm2 = ChatAnthropic(model_name="claude-2.0")

question = "What would be a good company name for a company that makes colorful socks?"

result1 = llm1.invoke(question)
result2 = llm2.invoke(question)

print("Result from OpenAI:", result1.content)
print("Result from Anthropic:", result2.content)