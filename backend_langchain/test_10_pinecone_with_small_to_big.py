
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import DirectoryLoader
from langchain.schema import Document
from langchain.text_splitter import NLTKTextSplitter

from pinecone import Pinecone
from uuid import uuid4
import nltk

# Initialize Pinecone (adjust to your specific environment and keys as needed)
pc = Pinecone()
index_name = 'research-paper-rag-index'
index = pc.Index(index_name)
index.describe_index_stats()

# Initialize OpenAI embeddings
embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")

# Wrap the Pinecone index with langchain's VectorStore
vector_store = PineconeVectorStore(index=index, embedding=embeddings)

# Load your text files
loader = DirectoryLoader('./', glob="*.txt")
documents = loader.load()

# Create a sentence splitter
sentence_splitter = NLTKTextSplitter()

all_sentence_docs = []
for doc in documents:
    # Split the entire document into sentences
    sentences = sentence_splitter.split_text(doc.page_content)

    # For each sentence, create a new Document with the sentence as content,
    # and the surrounding context (two sentences before and after) as metadata.
    for i, sentence in enumerate(sentences):
        # Identify the start and end of the context window
        start_ctx = max(0, i - 2)
        end_ctx = min(len(sentences), i + 3)
        surrounding = sentences[start_ctx:end_ctx]

        # Create a new Document
        sentence_doc = Document(
            page_content=sentence,
            metadata={
                "context": " ".join(surrounding),  # store the 2 before + current + 2 after as context
                "source": doc.metadata.get("source", ""),
            }
        )
        all_sentence_docs.append(sentence_doc)

# Generate unique IDs for each sentence
uuids = [str(uuid4()) for _ in range(len(all_sentence_docs))]

# Add the sentence Documents to your Pinecone vector store
vector_store.add_documents(documents=all_sentence_docs, ids=uuids)
