from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
from langchain.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate

system_template = "You are a helpful assistant that translates {input_language} to {output_language}."
human_template = "{text}"

final_prompt = ChatPromptTemplate.from_messages([
    ("system", system_template),
    ("human", human_template),
])

#print(final_prompt.format(
#    input_language="English", 
#    output_language="French", 
#    text="I love programming.",
#))

chat_model = ChatOpenAI()

chain = final_prompt | chat_model

result = chain.invoke(dict(
    input_language="English", 
    output_language="French", 
    text="I love programming.",
))

print(result.content)
