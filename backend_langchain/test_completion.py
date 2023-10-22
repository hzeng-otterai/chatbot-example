from langchain.llms import OpenAI


llm = OpenAI()

output = llm.predict("hi!\n")

print(output)