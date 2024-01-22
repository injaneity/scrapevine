from flask import Flask, request, jsonify
from seo import product_search
from webpage_to_image import get_image
from image_summary import encode_image, summarize_image
import json

api_key = 'AIzaSyC8JhE_upi0lFOpDmN5xTdna5Dzh_RBH5I'
pse_id = 'b4d45415c77044fae'

app = Flask(__name__)

@app.route('/receive_data', methods=['POST'])
def receive_data():
    # Get JSON data sent from the frontend
    data = request.get_json()
    
    # Log or process the data here
    print("Received data:", data)

    url = data['siteUrl']
    tags = data['tags']
    input_product_list = product_search(tags, url, api_key, pse_id)

    output_product_list = []

    for link in input_product_list:
        get_image(link)
        product_info = summarize_image(encode_image('webpage_screenshot.png'))
        product_dict = json.loads(product_info)
        product_dict[url] = link
        output_product_list.append(product_dict)

    sample_data = [
        {"headers": ["name", "colour", "price", "url"]},
        {"name": "Sport Running Shoes", "colour": "White", "price": "$89", "url": "https://example.com/product/sport-running-shoes"},
        {"name": "Smartphone X200", "colour": "Black", "price": "$299", "url": "https://example.com/product/smartphone-x200"},
        {"name": "Bluetooth Headphones E7", "colour": "Red", "price": "$79", "url": "https://example.com/product/bluetooth-headphones-e7"},
        {"name": "Leather Wallet Classic", "colour": "Brown", "price": "$35", "url": "https://example.com/product/leather-wallet-classic"},
        {"name": "Summer Dress Floral", "colour": "Blue", "price": "$49", "url": "https://example.com/product/summer-dress-floral"}
    ]

    # Respond back to the frontend with the sample JSON data
    return jsonify(output_product_list)



if __name__ == '__main__':
    app.run(debug=True)
