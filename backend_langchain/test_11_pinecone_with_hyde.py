from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings
from pinecone import Pinecone
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain import hub

from langchain.chains import HypotheticalDocumentEmbedder

pc = Pinecone()

index_name = 'research-paper-rag-index'
index = pc.Index(index_name)
index.describe_index_stats()

llm = ChatOpenAI(model_name='gpt-3.5-turbo', temperature=0.0)

text_field = "text"
base_embeddings = OpenAIEmbeddings(model='text-embedding-ada-002')
embeddings = HypotheticalDocumentEmbedder.from_llm(llm, base_embeddings, "web_search")

vectorstore = PineconeVectorStore(index, embeddings, text_field)

# Wrap the base retriever with HyDE
retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 6})

# Function to combine multiple returned documents
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# Pull an example prompt from the LangChain hub
prompt = hub.pull("rlm/rag-prompt")

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# Example usage
for chunk in rag_chain.stream("What is attention?"):
    print(chunk, end="", flush=True)

