
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import DirectoryLoader
from langchain.schema import Document
from langchain.text_splitter import NLTKTextSplitter

from pinecone import Pinecone
from uuid import uuid4
import nltk
#nltk.download('punkt')
#nltk.download('punkt_tab')
#nltk.download('averaged_perceptron_tagger')
#nltk.download('maxent_ne_chunker')
#nltk.download('words')
#from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get Pinecone API key
PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
#PINECONE_ENVIRONMENT = os.getenv('PINECONE_ENVIRONMENT')
pc = Pinecone(api_key=PINECONE_API_KEY)
# Initialize Pinecone (adjust to your specific environment and keys as needed)

index_name = 'research-paper-rag-index'
index = pc.Index(index_name)
index.describe_index_stats()

# Initialize OpenAI embeddings
embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")

# Wrap the Pinecone index with langchain's VectorStore
vector_store = PineconeVectorStore(index=index, embedding=embeddings)

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

# Load your text files
#loader = DirectoryLoader('./', glob="*.txt")
#documents = loader.load()


from langchain_text_splitters import RecursiveCharacterTextSplitter

import re

# Your existing initialization code remains the same...

# First split into sentences, then ensure each chunk is within size limit
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=4000,
    chunk_overlap=200,
    length_function=len,
    separators=["\n\n", "\n", ".", "!", "?", " ", ""]
)

all_sentence_docs = []
for doc in documents:
    # First split into manageable chunks
    chunks = text_splitter.split_text(doc.page_content)
    
    # For each chunk, create a Document with context
    for i, chunk in enumerate(chunks):
        # Identify the context window
        start_ctx = max(0, i - 2)
        end_ctx = min(len(chunks), i + 3)
        surrounding = chunks[start_ctx:end_ctx]
        
        # Create Document
        chunk_doc = Document(
            page_content=chunk,
            metadata={
                "context": " ".join(surrounding),
                "source": doc.metadata.get("source", ""),
            }
        )
        all_sentence_docs.append(chunk_doc)

# Generate unique IDs
uuids = [str(uuid4()) for _ in range(len(all_sentence_docs))]

# Add to vector store
vector_store.add_documents(documents=all_sentence_docs, ids=uuids)