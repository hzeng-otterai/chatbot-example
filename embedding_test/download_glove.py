import requests
import os

def download_glove(url, save_path):
    # Make a request to the URL
    response = requests.get(url, stream=True)
    
    # Open a local file with write-binary mode
    with open(save_path, "wb") as file:
        # Write the content to the file in chunks
        for chunk in response.iter_content(chunk_size=128):
            file.write(chunk)
    print(f"GloVe embeddings have been downloaded to {save_path}")

# URL for the GloVe embeddings with 50 dimensions
glove_url = "http://nlp.stanford.edu/data/glove.6B.zip"
# Path where you want to save the zip file
save_path = "glove.6B.zip"

download_glove(glove_url, save_path)
