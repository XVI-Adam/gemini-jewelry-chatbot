# generate an image consisting of all the ordered items for project 2

from google import genai
from google.genai import types
import base64
from dotenv import load_dotenv
import os

MODEL_ID = "gemini-2.0-flash-exp"

def gen_order_image(client, prompt):
    # Ask Gemini to generate a picture.  If none is generated return None
    # Otherwise the bytes representing the picture are returned
    response = client.models.generate_content(
            model=MODEL_ID,
            contents=prompt,
            config=types.GenerateContentConfig(response_modalities=['TEXT', 'IMAGE'])
    )
    for part in response.candidates[0].content.parts:
         if part.text is not None:
             print("TEXT PART:",part.text)  # for debugging
         elif part.inline_data is not None:
             print("image found")           # for debugging
             return base64.b64decode(part.inline_data.data)

    return None
         

def main():
    # for testing
    load_dotenv() # GEMINI_API_KEY should be defined in a .env file
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    gen_order_image(client, "Generate a picture of a dog")

if __name__ == "__main__":
    main()
