import google.generativeai as genai
#NEED API KEY
genai.configure(api_key = "")

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