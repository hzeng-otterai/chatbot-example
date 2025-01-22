from langchain.chains import ConversationalRetrievalChain
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os


# Load documents
loader = DirectoryLoader('./src/pdf', glob="*.pdf", loader_cls=PyPDFLoader)
documents = loader.load()

# Split documents into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
chunks = text_splitter.split_documents(documents)

print("Creating embeddings")
# Create embeddings for each chunk
embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(chunks, embeddings)
retriever = vectorstore.as_retriever()

print("Creating chains")
llm = ChatOpenAI(streaming=True)  # Added streaming for web interface
memory = ConversationBufferMemory(
    memory_key="chat_history", 
    return_messages=True, 
    output_key="answer"
    )
conversation = ConversationalRetrievalChain.from_llm(
    llm, 
    retriever=retriever, 
    memory=memory, 
    verbose=True,
    return_source_documents=True,  # Added to track sources
    output_key="answer"
)

def call_chat(question):
    """Function to be used by Flask views"""
    # Get response with source documents
    result = conversation.invoke({"question": question})
    answer = result["answer"]
    sources = result.get("source_documents", [])

    # Add source information
    source_info = "\n\nSources:"
    for doc in sources:
        source = doc.metadata.get('source', 'Unknown')
        page = doc.metadata.get('page', 'unknown')
        source_info += f"\n- {source}, page {page}"

    full_response = answer + source_info

    # Stream response word by word
    for chunk in full_response.split():
        yield {"token": chunk + " "}

# Keep the CLI interface for testing
if __name__ == "__main__":
    while True:
        user_input = input("> ")
        result = conversation.invoke(user_input)
        print(result["answer"])