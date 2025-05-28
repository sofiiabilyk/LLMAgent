import openai
import numpy as np
from openai import OpenAI

OPENAI_API_KEY = ""
openai.api_key = OPENAI_API_KEY
client = OpenAI(api_key=OPENAI_API_KEY)


def get_embedding(text, model="text-embedding-3-small"):
    response = client.embeddings.create(
        input=text,
        model=model
    )
    return response.data[0].embedding

def cosine_similarity(vec1, vec2):
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))


#read the generated example
with open('C:/Projects/git/Domu/generated_example.txt', 'r', encoding='utf-8') as file:
    generated_example = file.read()
    
#read the original example
with open('C:/Projects/git/Domu/original_example.txt', 'r', encoding='utf-8') as file:
    original_example = file.read()

#get the embeddings of the generated example and the original example
embedding1 = get_embedding(generated_example)
embedding2 = get_embedding(original_example)

#calculate the cosine similarity between the two embeddings
similarity = cosine_similarity(embedding1, embedding2)
print(f"Cosine similarity: {similarity}")
