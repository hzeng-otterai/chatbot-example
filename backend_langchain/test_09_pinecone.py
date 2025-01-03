from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings
from pinecone import Pinecone

pc = Pinecone()

index_name = 'research-paper-rag-index'
index = pc.Index(index_name)
index.describe_index_stats()

llm = ChatOpenAI(
    model_name='gpt-3.5-turbo',
    temperature=0.0
)

text_field = "text"
embeddings = OpenAIEmbeddings(model='text-embedding-ada-002')
vectorstore = PineconeVectorStore(index, embeddings, text_field)

qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever()
)

query = "What is Attention?"

result = qa.invoke(query)
print(result["result"])