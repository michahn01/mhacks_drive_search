import google.generativeai as genai

genai.configure(api_key = "AIzaSyCB2vqDZPG-c5RoqEns1zJxzobfZISBlc8")
# https://cloud.google.com/vertex-ai/generative-ai/docs/embeddings/get-multimodal-embeddings

# returns embeddings for item we want to store
def generateTextEmbeddings(text='', model='models/text-embedding-004'):
    result = genai.embed_content(model=model,
                                 content=text,
                                 task_type='retrieval_document')
    return result

# returns embeddings for the search query
def generateQueryEmbeddings(text='', model='models/text-embedding-004'):
    result = genai.embed_content(model=model,
                                 content=text,
                                 task_type='retrieval_query')
    return result

def textEmbeddingDemo():
    test_str = 'I have a computer'
    res = generateTextEmbeddings(text=test_str)
    print(res)


if __name__ == "__main__":
    textEmbeddingDemo()

