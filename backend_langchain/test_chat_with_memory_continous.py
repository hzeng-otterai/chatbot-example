from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI

llm = ChatOpenAI()
conversation = ConversationChain(llm=llm, verbose=True)

while(True):
    user_input = input("> ")

    result = conversation({"input": user_input})

    print(result["response"])