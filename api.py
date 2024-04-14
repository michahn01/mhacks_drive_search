from flask import Flask, request, jsonify
from textEmbedding import generateQueryEmbeddings
from flask_cors import CORS
import numpy as np

import json

app = Flask(__name__)
CORS(app)

file_links = {
   "/content/drive/My Drive/pic1.jpeg": "https://drive.google.com/file/d/1SNv-cgJ0WhfB_nQIxONSE1EubxntZyLG/view?usp=drive_link",
   "/content/drive/My Drive/pic2.png": "https://drive.google.com/file/d/1nNCZiv7YnzBr5zA9GQ-WvD1AJFC9jPtD/view?usp=drive_link",
   "/content/drive/My Drive/pic3.webp": "https://drive.google.com/file/d/1uLgxFsqq9wOpN4VSYl32r4YOYjrAb8wt/view?usp=drive_link",
   "/content/drive/My Drive/pic4.webp": "https://drive.google.com/file/d/15lDeP7S1cbB6zrAHLDrYKjq9aRk3rPqh/view?usp=drive_link",
   "/content/drive/My Drive/pic5.jpg": "https://drive.google.com/file/d/1KkWJ1BGPlWb5pcYVCeciPXvuzO9hMMAY/view?usp=drive_link",
   "/content/drive/My Drive/pic6.jpg": "https://drive.google.com/file/d/1Vjf56nyTXtlvRF0kujbGHDSzNTLxOSkB/view?usp=drive_link",
   "/content/drive/My Drive/pic7.jpg": "https://drive.google.com/file/d/1XbzybRRJHjTCjbrmOMgHtCeThQ4Fddx7/view?usp=drive_link",
   "/content/drive/My Drive/pic8.webp": "https://drive.google.com/file/d/1bEYWscttnvOdA6mW1rTxAFUDCWlv20Wo/view?usp=drive_link",
   "/content/drive/My Drive/pic9.jpg": "https://drive.google.com/file/d/1TigZeQ-XQvVBESjHWr_OWnCGLahzndMR/view?usp=drive_link",
   "/content/drive/My Drive/pic10.jpg": "https://drive.google.com/file/d/116bfK4PETbBPeztXZL3BBGUjjWvzEMB5/view?usp=drive_link",
   "/content/drive/My Drive/pic11.jpg": "https://drive.google.com/file/d/1vWKdOOX4D5YGWQoXSfuNTox5dX6WZWoP/view?usp=drive_link",
   "/content/drive/My Drive/pic12.jpg": "https://drive.google.com/file/d/1rXku6LYflAYfpzp35fUJddw5g0HNOeaK/view?usp=drive_link",
   "/content/drive/My Drive/pic13.jpg": "https://drive.google.com/file/d/1RfHFHToMFrqBfRxPwq2V_iGwSlHmaOov/view?usp=drive_link",
   "/content/drive/My Drive/pic14.jpg": "https://drive.google.com/file/d/12GAdZczuBpx4M1pE0rwFKalQ0w3raSKf/view?usp=drive_link",
   "/content/drive/My Drive/pic15.jpg": "https://drive.google.com/file/d/1eywZCwj2lQW-jyRmTXC_KhCCZy8HvwZ2/view?usp=drive_link",
   "/content/drive/My Drive/pic16.webp": "https://drive.google.com/file/d/19X4QbAZgscJanfBOuQwpvhcd-sgOevQt/view?usp=drive_link",
   "/content/drive/My Drive/pic17.jpg": "https://drive.google.com/file/d/16hE2H-JybNyXmM3gB2Lsrk_2nmMuRMiz/view?usp=drive_link",
   "/content/drive/My Drive/pic18.jpg": "https://drive.google.com/file/d/1ABvpyMMox0tAYjenACXm69pHyufvmWTb/view?usp=drive_link",
   "/content/drive/My Drive/pic19.png": "https://drive.google.com/file/d/1eobq9NsuRp3bgM_gHigC5T8UCxbCyjJs/view?usp=drive_link",
   "/content/drive/My Drive/vid1.mp4": "https://drive.google.com/file/d/1KC83tbxdv6d658I-Zqw2IOZ3P7uxym7K/view?usp=drive_link",
   "/content/drive/My Drive/vid2.mp4": "https://drive.google.com/file/d/1St8ktLr8ouM5eOGFIV_e1N3iOrNK4s-t/view?usp=drive_link",
   "/content/drive/My Drive/vid3.mp4": "https://drive.google.com/file/d/1aDsok1EIWkBsQK4eMa9p7A0hwVrgbIBP/view?usp=drive_link",
   "/content/drive/My Drive/vid4.mp4": "https://drive.google.com/file/d/1zXF-l87OTZ0NQe2yU1hcUOMHRlVfJMwj/view?usp=drive_link",
   "/content/drive/My Drive/vid5.mp4": "https://drive.google.com/file/d/13ck1j0qYOXsFoyxdTC1eFrbqzVoN8uZo/view?usp=drive_link",
   "/content/drive/My Drive/vid6.mp4": "https://drive.google.com/file/d/1WyVDgtYkVr1FPCM3MYw8A8_bNh_pTIYX/view?usp=drive_link",
   "/content/drive/My Drive/vid7.mp4": "https://drive.google.com/file/d/1IRuoIoLNFuwdDFuuM8y4RIQLBLgJPwe1/view?usp=drive_link",
   "/content/drive/My Drive/vid8.mp4": "https://drive.google.com/file/d/1gQJfVINst8oZLRwo-HelT-92xWlXoIm8/view?usp=drive_link"
}


def cosine_similarity(vec1, vec2):
   dot_product = np.dot(vec1, vec2)
   norm_vec1 = np.linalg.norm(vec1)
   norm_vec2 = np.linalg.norm(vec2)
   similarity = dot_product / (norm_vec1 * norm_vec2)
   return similarity

@app.route('/', methods=['PUT'])
def fetchResource():
   data = request.get_json()  # This method is ideal for parsing JSON data
   userquery = data.get('inputText', '')
   query = generateQueryEmbeddings(userquery)['embedding']
   with open('embedding_space.json', 'r') as json_file:
       embeddings = json.load(json_file)
   
   arr = []
   for i in range(len(embeddings)):
       print('index', i, embeddings[i])
       embedding = np.array(embeddings[i][0]['embedding'])
       file_path = embeddings[i][1]
       arr.append((cosine_similarity(embedding, query), file_path))
   arr.sort(reverse=True)


   arr = [file_links[a[1]] for a in arr[:5] if a[0] > 0.1]
   if len(arr) == 0:
       arr = ["No files found for that description!"]
   return jsonify({'links': arr})

if __name__ == '__main__':
    app.run(debug=True)