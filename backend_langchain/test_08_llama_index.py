import os.path
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage,
)

# check if storage already exists
PERSIST_DIR = "./storage"
if not os.path.exists(PERSIST_DIR):
    print("Loading the documents and creating the index")
    input_file_list = ["attention.txt", "few_shot.txt", "instruct_gpt.txt"]
    documents = SimpleDirectoryReader("./", input_files=input_file_list).load_data()
    index = VectorStoreIndex.from_documents(documents)
    print("Storing it for future use")
    index.storage_context.persist(persist_dir=PERSIST_DIR)
else:
    print("Loading the existing index")
    storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
    index = load_index_from_storage(storage_context)

# Either way we can now query the index
query_engine = index.as_query_engine()
response = query_engine.query("How big is GPT-3?")
print(response)