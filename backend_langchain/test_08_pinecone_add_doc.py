from pinecone import Pinecone
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get Pinecone API key
PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
#PINECONE_ENVIRONMENT = os.getenv('PINECONE_ENVIRONMENT')
pc = Pinecone(api_key=PINECONE_API_KEY)
index_name = 'research-paper-rag-index'

# Check if index exists, if not create it
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=1536,  # dimension for text-embedding-ada-002
        metric='cosine',
        spec={
            "serverless": {
                "cloud": "aws",
                "region": "us-east-1"  # or another supported region
            }
        }
    )

index = pc.Index(index_name)
index.describe_index_stats()

from langchain_openai import OpenAIEmbeddings
embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")

from langchain_pinecone import PineconeVectorStore
vector_store = PineconeVectorStore(index=index, embedding=embeddings)


from uuid import uuid4

from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
#import os
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

#loader = DirectoryLoader('./', glob="*.txt")
#documents = loader.load()
# Split documents into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
document_chunks = text_splitter.split_documents(documents)

uuids = [str(uuid4()) for _ in range(len(document_chunks))]

vector_store.add_documents(documents=document_chunks, ids=uuids)
