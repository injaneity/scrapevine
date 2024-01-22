import base64
from openai import OpenAI
import os

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

client = OpenAI(api_key='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')

def summarize_image(encoded_image):
    summary = client.chat.completions.create(
    model = "gpt-4-vision-preview",
    messages=[
        {
        "role": "user",
        "content": [
            {"type": "text", "text": 
            """Your role is to analyse screenshots of clothing products in online stores. Output the type of clothing (with short details), its colour, and its price (including decimals).
            Output in this format: ("type": "insert type", "colour": "insert colour", "price": "insert price"}"""},
            {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{encoded_image}",
            },
            },
        ],
        }
    ],
    max_tokens = 100,
    temperature = 0,
    top_p = 0,
    )
    return (summary.choices[0].message.content)
