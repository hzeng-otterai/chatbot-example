from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage

chat_model = ChatOpenAI()

text = "What would be a good company name for a company that makes colorful socks?"
messages = [HumanMessage(content=text)]

result = chat_model.predict_messages(messages)

print(result)
