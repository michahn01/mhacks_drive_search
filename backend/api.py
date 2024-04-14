from flask import Flask, request, jsonify
from textEmbedding import generateQueryEmbeddings
from flask_cors import CORS
import numpy as np

app = Flask(__name__)
CORS(app)

def cosine_similarity(vec1, vec2):
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    similarity = dot_product / (norm_vec1 * norm_vec2)
    return similarity


@app.route('/', methods=['GET'])
def fetchResource():
    query = generateQueryEmbeddings(request.args.get('query', ''))['embedding']
    embeddings = np.load('embedding_space.npy', allow_pickle=True)
    arr = []
    for i in range(len(embeddings)):
        embedding = np.array(embeddings[i][0]['embedding'])
        file_path = embeddings[i][1]
        arr.append((cosine_similarity(embedding, query), file_path))
    arr.sort()
    print(len(arr))
    return arr[:5]

if __name__ == '__main__':
    app.run(debug=True)