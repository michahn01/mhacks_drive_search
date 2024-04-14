import numpy as np
from imageEmbedding import generateImageEmbeddings

embeddings = np.load('embeddings.npy')

print(embeddings)

# new_embeddings = np.append(embeddings, [generateImageEmbeddings('image.png')], axis=0)

# np.save('embeddings.npy', new_embeddings)
