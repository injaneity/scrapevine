import base64
from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

client = OpenAI(api_key=os.getenv('GPT_API'))

def summarize_image(encoded_image):
    summary = client.chat.completions.create(
    model = "gpt-4-vision-preview",
    messages=[
        {
        "role": "user",
        "content": [
            {"type": "text", "text": "Output only the color and type of clothing product (with short details) and its price (converted to Singaporean dollars and including decimals), in the format: 'insert colour and type', 'insert S$'price''"},
            {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{encoded_image}",
            },
            },
        ],
        }
    ],
    temperature = 0,
    top_p = 0,
    )
    return (summary.choices[0].message.content)
