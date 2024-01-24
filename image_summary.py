import base64
from openai import OpenAI
import os

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

client = OpenAI(api_key=os.getenv('GPT_API'))

def summarize_image(encoded_image, data_requirements):

    requirements_dict = {}
    for requirement in  data_requirements:
        requirements_dict[requirement] = f"insert {requirement}"

    summary = client.chat.completions.create(
    model = "gpt-4-vision-preview",
    messages=[
        {
        "role": "user",
        "content": [
            {"type": "text", "text": 
            f"""Your role is to analyse screenshots of clothing products in online stores, 
            and output the necessary characteristics to fill up the following format: {requirements_dict}. 
            For price, output only the numeric value. 
            If unable to provide all characteristics, output only an empty python dictionary instead."""},
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
    print(summary.choices[0].message.content)
    return (summary.choices[0].message.content)
