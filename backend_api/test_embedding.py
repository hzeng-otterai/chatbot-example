from openai import OpenAI
import numpy as np

def cosine_similarity(vector1, vector2):
    dot_product = np.dot(vector1, vector2)
    norm_v1 = np.linalg.norm(vector1)
    norm_v2 = np.linalg.norm(vector2)
    return dot_product / (norm_v1 * norm_v2)

client = OpenAI()

input1 = "The food was delicious and the waiter is nice."
input2 = "I will never go there any more."
input3 = "They have good cook. And people are friendly."

response = client.embeddings.create(
  model="text-embedding-3-large",
  input=[input1, input2, input3],
  encoding_format="float"
)
e1 = response.data[0].embedding
e2 = response.data[1].embedding
e3 = response.data[2].embedding


print(e1, e2, e3)
print(cosine_similarity(e1, e2))
print(cosine_similarity(e2, e3))
print(cosine_similarity(e1, e3))
