#COMPANY THAT WE ARE PLAGARIZING/////////////
#https://www.shade.inc/


"""
What I think we need to implement, in order:
1) FOR EVERYTHING: A function that makes a call to Gemini to convert words (sentences, strings, anything) into word embeddings.
2) FOR IMAGES: A function thhat calls Gemini to create a detailed summary of the image

Basic Proces
1. Mount Google Drive
1b. choose specific folder in google drive
2. bundle all images/video as a group of tokens
3. Use bundle as input to Gemini
4. Output file name and path of best matches
5. Query file names and output to user (frontend)

"""

import google.generativeai as genai, os
import google.ai.generativelanguage as glm
import pydrive2
import chromadb
from chromadb import Documents, EmbeddingFunction, Embeddings
import numpy as np
import pandas as pd

api_key = 'AIzaSyCB2vqDZPG-c5RoqEns1zJxzobfZISBlc8'#use this os.getenv('API_KEY'),in terminal set API_KEY=...
genai.configure(api_key = api_key)


from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

gauth = GoogleAuth()
gauth.LocalWebserverAuth()

drive = GoogleDrive(gauth)


# 1. Mount Google Drive



# 1b. choose specific folder in google drive

# documents = 

# 2. Create vector db, pass in folder (documents)

class GeminiEmbeddingFunction(EmbeddingFunction):
  def __call__(self, inputs: Documents) -> Embeddings:
    model = 'models/text-embedding-004'
    title = "Add Documents Query"
    return genai.embed_content(model=model,
                                content=inputs,
                                task_type="retrieval_document",
                                title=title)["embedding"]

def create_chroma_db(documents, name):
  chroma_client = chromadb.Client()
  db = chroma_client.create_collection(name=name, embedding_function=GeminiEmbeddingFunction())

  for i, d in enumerate(documents):
    db.add(
      documents=d,
      ids=str(i)
    )
  return db

db = create_chroma_db(documents, "googlecarsdatabase")

def get_relevant_passage(query, db):
  passage = db.query(query_texts=[query], n_results=1)['documents'][0][0]
  return passage

# Perform embedding search
passage = get_relevant_passage("touch screen features", db)
Markdown(passage)


def make_prompt(query, relevant_passage):
  escaped = relevant_passage.replace("'", "").replace('"', "").replace("\n", " ")
  prompt = ("""You are a helpful and informative bot that answers questions using text from the reference passage included below. \
  Be sure to respond in a complete sentence, being comprehensive, including all relevant background information. \
  However, you are talking to a non-technical audience, so be sure to break down complicated concepts and \
  strike a friendly and converstional tone. \
  If the passage is irrelevant to the answer, you may ignore it.
  QUESTION: '{query}'
  PASSAGE: '{relevant_passage}'

    ANSWER:
  """).format(query=query, relevant_passage=escaped)

  return prompt
# query = "How do you use the touchscreen in the Google car?"
# prompt = make_prompt(query, passage)
# Markdown(prompt)





# 3. Use bundle as input to Gemini

# 4. Output file name and path of best matches

# 5. Query file names and output to user (frontend)
