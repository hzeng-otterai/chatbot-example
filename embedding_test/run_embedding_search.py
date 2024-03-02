import numpy as np
import sys
from scipy import spatial
from scipy.spatial.distance import cdist
import zipfile
import time

zip_path = "glove.6B.zip"  # Update this path to where you've stored the GloVe zip file
embedding_file_name = "glove.6B.50d.txt"  # Update if using a different GloVe embedding file

#np.show_config()

def load_glove_embeddings_from_zip(zip_path, embedding_file_name):
    embeddings_dict = {}
    with zipfile.ZipFile(zip_path, 'r') as z:
        with z.open(embedding_file_name) as file:
            for line in file:
                line = line.decode('utf-8')  # Decode bytes to string
                values = line.split()
                word = values[0]
                vector = np.asarray(values[1:], "float32")
                embeddings_dict[word] = vector
    return embeddings_dict

def build_matrix_and_word_list():
    vocab_size = len(embeddings_dict)
    vector_size = len(next(iter(embeddings_dict.values())))
    embedding_matrix = np.zeros((vocab_size, vector_size))
    words = []
    
    for i, (word, vector) in enumerate(embeddings_dict.items()):
        embedding_matrix[i] = vector
        words.append(word)
    
    return embedding_matrix, words

def normalize_vectors(vectors):
    norms = np.linalg.norm(vectors, axis=1, keepdims=True)
    return vectors / norms

embeddings_dict = load_glove_embeddings_from_zip(zip_path, embedding_file_name)
embedding_matrix, words = build_matrix_and_word_list()
normalized_embedding_matrix = normalize_vectors(embedding_matrix)

print(f"GloVe embeddings loaded. Totally {len(embeddings_dict)} words. Type a word to find similar words, or type 'exit' to quit.")

def find_similar_words_enumerate(input_word, top_n=10):
    if input_word not in embeddings_dict:
        return None
    input_vec = embeddings_dict[input_word]
    distances = {}

    for word, vector in embeddings_dict.items():
        if word == input_word:
            continue
        sim = 1 - spatial.distance.cosine(input_vec, vector)
        distances[word] = sim

    return sorted(distances.items(), key=lambda item: item[1], reverse=True)[:top_n]

def find_similar_words_with_dot(input_word, top_n=10):
    if input_word not in embeddings_dict:
        print("Word not found in GloVe embeddings.")
        return []

    input_vec = embeddings_dict[input_word]
    input_vec_normalized = input_vec / np.linalg.norm(input_vec)
    
    # Compute cosine similarity with dot product
    cosine_similarities = np.dot(normalized_embedding_matrix, input_vec_normalized)
    
    # Find the top N similar words
    top_indices = np.argsort(cosine_similarities)[-top_n:][::-1]
    return [(words[i], cosine_similarities[i]) for i in top_indices]

if __name__ == "__main__":

    while True:
        input_word = input("Enter a word: ").strip()
        if input_word.lower() == 'exit':
            print("Exiting program.")
            break

        start_time = time.time()
        #similar_words = find_similar_words_enumerate(input_word)
        similar_words = find_similar_words_with_dot(input_word)
        end_time = time.time()
        if similar_words:
            print(f"Top 10 similar words {end_time-start_time:.2f} seconds used:")
            for word, similarity in similar_words:
                print(f"{word}: {similarity}")
        else:
            print("No similar words found or word not in embeddings.")
