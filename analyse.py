import json
from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(api_key=os.getenv('GPT_API'))

def analyse_html(data, keywords):
    
    keyword_dict = {}
    for keyword in keywords:
        keyword_dict[keyword] = f"insert {keyword}"

    analysis = client.chat.completions.create(
    model = "gpt-4-0125-preview",
    messages=[
    {"role": "system",
    "content":
    f"""Your role is to analyse html from webpages containing clothing products, 
            and output the necessary characteristics to fill up the following format: {keyword_dict}. 
            For price, output only the numeric value. If there are multiple prices, output the median price.
            If unable to provide all characteristics, do not output any explanation - output only an empty dictionary instead."""},
    {"role": "user",
    "content": f"{data}"},
    ],
    max_tokens = 400,
    temperature = 0,
    top_p = 0,
    )
    return (analysis.choices[0].message.content)

def analyse_trend(data):

    analysis = client.chat.completions.create(
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
    "content": f"{data}"},
    ],
    max_tokens = 400,
    temperature = 0,
    top_p = 0,
    )

    return (analysis.choices[0].message.content)

def analyse_price(data):
    prices = [float(product["Price"]) for product in data if product["Price"]]
    price_dict = {
        "Average Price": f"{round(sum(prices) / len(prices), 2):.2f}" if prices else "0.00",
        "Highest Price": f"{round(max(prices), 2):.2f}" if prices else "0.00",
        "Lowest Price": f"{round(min(prices), 2):.2f}" if prices else "0.00"
    }
    return price_dict


