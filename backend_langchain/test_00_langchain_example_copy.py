from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain import hub
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

# Split documents into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = text_splitter.split_documents(documents)

# Create embeddings for each chunk
vectorstore = Chroma.from_documents(chunks, OpenAIEmbeddings())

# Define a retriever from the vector DB
retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 6})

# Get a prompt from LangChain hub
prompt = hub.pull("rlm/rag-prompt")

# Define the LLM object using OpenAI
llm = ChatOpenAI(model_name="gpt-4o", temperature=0)

# The function to combine multiple documents into one
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# Define whole chain
rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# Run the query
result = rag_chain.invoke("What is attention?")
print(result)