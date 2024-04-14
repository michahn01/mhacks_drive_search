import google.generativeai as genai
from PIL import Image

genai.configure(api_key = "")

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
