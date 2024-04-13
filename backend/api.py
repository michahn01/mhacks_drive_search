from flask import Flask, request, jsonify
from textEmbedding import generateQueryEmbeddings

@app.route('/', methods=['GET'])
def fetchResource():
    query = generateQueryEmbeddings(request.args.get('query', ''))
    return

if __name__ == '__main__':
    app = Flask(__name__)
    app.run(debug=True)