from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    HumanMessage,
)


from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
chat = ChatOpenAI(streaming=True, callbacks=[StreamingStdOutCallbackHandler()], temperature=0)
resp = chat.generate([[HumanMessage(content="what is 2+4?")]])

print(resp)