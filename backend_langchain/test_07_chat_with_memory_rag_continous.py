from langchain.chains import ConversationalRetrievalChain
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory, ConversationSummaryMemory
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
import os
# Get list of text files
txt_files = [f for f in os.listdir('./text') if f.endswith('.txt')]

# Load documents using TextLoader with proper encoding
documents = []
for file_name in txt_files:
    file_path = os.path.join('./text', file_name)
    try:
        # Try UTF-8 first
        loader = TextLoader(file_path, encoding='utf-8', autodetect_encoding=True)
        docs = loader.load()
    except UnicodeDecodeError:
        # Fallback to latin-1 if UTF-8 fails
        loader = TextLoader(file_path, encoding='latin-1')
        docs = loader.load()
    documents.extend(docs)
#print("Loading documents")
# Loading documents from local disk
#loader = DirectoryLoader('./', glob="*.txt")
#
# documents = loader.load()

# Split documents into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
chunks = text_splitter.split_documents(documents)

print("Creating embeddings")
# Create embeddings for each chunk
embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(chunks, embeddings)
retriever = vectorstore.as_retriever()

print("Creating chains")
llm = ChatOpenAI()
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
conversation = ConversationalRetrievalChain.from_llm(
    llm, retriever=retriever, memory=memory, verbose=True)

while(True):
    user_input = input("> ")
    result = conversation.invoke(user_input)
    print(result["answer"])