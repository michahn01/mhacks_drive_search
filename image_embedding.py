"""
What I think we need to implement, in order:
1) FOR EVERYTHING: A function that makes a call to Gemini to convert words (sentences, strings, anything) into word embeddings.
2) FOR IMAGES: A function thhat calls Gemini to create a detailed summary of the image
                Use img embedding model?
"""
import google.generativeai as genai
import PIL.Image

#Setup
genai.configure(api_key = "AIzaSyCB2vqDZPG-c5RoqEns1zJxzobfZISBlc8")
instruction = "Generate 5 words that list objects in the image, and 5 words that capture more nuanced concepts/ideas in the image. List just the words, all on one line, with a space separating each word, no titles, no words or characters other than the 10 words"
#model = genai.GenerativeModel('gemini-pro-vision', system_instruction=instruction)
model = genai.GenerativeModel('gemini-1.5-pro-latest', system_instruction=instruction)

#Run Query
img = PIL.Image.open('image.jpg') #NEED TO GET FROM GOOGLE DRIVE
prompt = []
response = model.generate_content([prompt,img])
words = response.split()

#Generate Embeddings
for word in words:
    embedding = genai.embed_content(
        model="models/text-embedding-004",
        content=word,
        task_type="semantic_similarity")
    
#TODO: add to database and query

    





