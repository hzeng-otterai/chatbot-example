from langchain_community.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
from langchain.prompts.chat import ChatPromptTemplate

chat_model = ChatOpenAI()

system_template = "You are a helpful assistant that translates {input_language} to {output_language}."
human_template = "{text}"

chat_prompt_template = ChatPromptTemplate.from_messages([
    ("system", system_template),
    ("human", human_template),
])

messages = chat_prompt_template.format_messages(input_language="English", output_language="French", text="I love programming.")

result = chat_model.invoke(messages)

print(result.content)
