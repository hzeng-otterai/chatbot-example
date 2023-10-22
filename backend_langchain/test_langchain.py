from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter



def generate_response(file_names, query_text):
    loader = DirectoryLoader('./', glob="*.txt")
    documents = loader.load()

    # Split documents into chunks
    text_splitter = CharacterTextSplitter(separator="\n", chunk_size=1000, chunk_overlap=0)
    chunks = text_splitter.split_documents(documents)

    # Create embeddings for each chunk
    embeddings = OpenAIEmbeddings()
    vectorstore = Chroma.from_documents(chunks, embeddings)

    # Use QA chain to retrieve relevant chunks
    llm = OpenAI(model_name='text-davinci-003')
    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=vectorstore.as_retriever())
    result = qa_chain({"query": query_text})

    return result["result"]


if __name__ == "__main__":
    file_names = ["attention.txt", "few_shot.txt", "instruct_gpt.txt"]

    r = generate_response(file_names, "What papers are related to large language model?")

    print(r)