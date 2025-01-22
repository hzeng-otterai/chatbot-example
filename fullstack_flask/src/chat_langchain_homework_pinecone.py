from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain_pinecone import PineconeVectorStore
from langchain.chains import ConversationalRetrievalChain
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pinecone import Pinecone
from .models import db, ChatMessage
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize Pinecone
PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
pc = Pinecone(api_key=PINECONE_API_KEY)

# Initialize index
index_name = 'langchain-retrieval-augmentation-fast'
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=1536,
        metric='cosine',
        spec={
            "serverless": {
                "cloud": "aws",
                "region": "us-east-1"
            }
        }
    )

# Load and process documents
loader = DirectoryLoader('./src/pdf', glob="*.pdf", loader_cls=PyPDFLoader)
documents = loader.load()
    
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
chunks = text_splitter.split_documents(documents)
   
# Initialize vector store
index = pc.Index(index_name)
embeddings = OpenAIEmbeddings(model='text-embedding-ada-002')
vectorstore = PineconeVectorStore(index, embeddings, "text")

# Load documents into vector store
vectorstore.add_documents(chunks)

# Create conversation chain
llm = ChatOpenAI(streaming=True)
memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        output_key="answer"
    )
conversation = ConversationalRetrievalChain.from_llm(
        llm,
        retriever=vectorstore.as_retriever(),
        memory=memory,
        verbose=True,
        return_source_documents=True,
        output_key="answer"
    )
    

# Chat function with streaming and DB storage
def call_chat(question):
    result = conversation.invoke({"question": question})
    
    answer = result["answer"]
    sources = result.get("source_documents", [])
    
    # Add source information to the answer
    source_info = "\n\nSources:"
    for doc in sources:
        source = doc.metadata.get('source', 'Unknown')
        page = doc.metadata.get('page', 'unknown')
        source_info += f"\n- {source}, page {page}"
    
    full_response = answer + source_info
    
    # Stream the response
    for chunk in full_response.split():
        yield {"token": chunk + " "}
    
    # Save to database with source information
    chat_message = ChatMessage(
        user_id=1,
        question=question,
        answer=full_response
    )
    db.session.add(chat_message)
    db.session.commit()