from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain_pinecone import PineconeVectorStore
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough
from langchain.chains import ConversationalRetrievalChain
from pinecone import Pinecone

from .models import db, ChatMessage

pc = Pinecone()

print("Connecting to Pinecone index")
index_name = 'langchain-retrieval-augmentation-fast'
index = pc.Index(index_name)
index.describe_index_stats()

text_field = "text"
embeddings = OpenAIEmbeddings(model='text-embedding-ada-002')
vectorstore = PineconeVectorStore(index, embeddings, text_field)

print("Creating chains")
template = """You are a helpful assistant. I will give you a list of articles with title and text. Please answer questions.
Articles:
{context}

Question: {question}
"""
prompt = ChatPromptTemplate.from_template(template)

llm = ChatOpenAI(streaming=True)
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
retriever = vectorstore.as_retriever()

retrieval_chain = (
    {
        "context": retriever.with_config(run_name="Docs"),
        "question": RunnablePassthrough(),
    }
    | prompt
    | llm
    | StrOutputParser()
)

def call_chat(question):
    answer = ""
    for chunk in retrieval_chain.stream(question):
        answer += chunk
        yield {"token": chunk}

    chat_message = ChatMessage(user_id=1, question=question, answer=answer)
    db.session.add(chat_message)
    db.session.commit()

