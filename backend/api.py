from flask import Flask, request, jsonify

# returns embeddings for the search query
def generateQueryEmbeddings(text='', model='models/text-embedding-004'):
    result = genai.embed_content(model=model,
                                 content=text,
                                 task_type='retrieval_query')
    return result

# returns embeddings for item we want to store
def generateTextEmbeddings(text='', model='models/text-embedding-004'):
    result = genai.embed_content(model=model,
                                 content=text,
                                 task_type='retrieval_document')
    return result

@app.route('/', methods=['GET'])
def fetchResource():
    return

if __name__ == '__main__':
    app = Flask(__name__)
    app.run(debug=True)