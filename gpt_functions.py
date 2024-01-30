import base64
from openai import OpenAI
import os

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

client = OpenAI(api_key='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')

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
            For price, convert to Singaporean dollars if necessary, and output only the numeric value. 
            If unable to provide all characteristics, do not output any explanation - output only an empty dictionary instead."""},
            {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{encoded_image}",
                "detail": "high"
            },
            },
        ],
        }
    ],
    max_tokens = 200,
    temperature = 0,
    top_p = 0,
    )

    print(summary.choices[0].message.content)
    return (summary.choices[0].message.content)

def analyse_trend(data_json):

    summary = client.chat.completions.create(
    model = "gpt-4-0125-preview",
    messages=[
    {"role": "system",
    "content":
    """You will be given JSON that contains a list of information about clothing products in a specific market.
    For example, such information can include the price of a product, its colour, or the type of clothing it is.
    Your role is to understand this information and conduct market analysis. Your analysis should be useful in helping businesspeople enter the given market.
    Output any trends in the data that you find. For example, such trends can include finding which characteristic appears most frequently across the list of products provided.
    Do not provide comment on the URLs listed.
    Do not provide comment on the highest, lowest, and average price.
    Your analysis should be comprehensive, including explanation of data and detailed potential insights.
    The output must start with: 'Brief Analysis:', must be in plain text (do not use newline characters), and must use a maximum of 400 tokens."""},
    {"role": "user",
    "content": f"{data_json}"},
    ],
    max_tokens = 400,
    temperature = 0,
    top_p = 0,
    )

    print(summary.choices[0].message.content)
    return (summary.choices[0].message.content)
