"""
What I think we need to implement, in order:
1) FOR EVERYTHING: A function that makes a call to Gemini to convert words (sentences, strings, anything) into word embeddings.
2) FOR IMAGES: A function thhat calls Gemini to create a detailed summary of the image
                Use img embedding model?
"""
import google.generativeai as genai
from PIL import Image

genai.configure(api_key = "AIzaSyCB2vqDZPG-c5RoqEns1zJxzobfZISBlc8")

def generateImageEmbeddings(img_path):
    prompt = "Generate 5 words that list objects in the image, and 5 words that capture more nuanced concepts/ideas in the image. List just the words, all on one line, with a space separating each word, no titles, no words or characters other than the 10 words"
    img = Image.open(img_path)
    genai.upload_file(path=img_path)
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([prompt, img]).text

    embedding = genai.embed_content(
        model="models/text-embedding-004",
        content=response,
        task_type="retrieval_document")
    return embedding

if __name__ == "__main__":
    print(generateImageEmbeddings('image.png'))