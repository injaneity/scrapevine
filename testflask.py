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
    data_requirements = data['dataRequirements']

    # input_product_list = product_search(tags, url, api_key, pse_id)
    input_product_list = ['https://www.lovebonito.com/sg/mira-knit-midi-dress.html', 'https://www.pazzion.com/collections/shoes-flats/products/elaia-point-toe-ballerina-flats?variant=42287420899571']

    output_product_list = []

    for link in input_product_list:
        get_image(link)
        product_info = summarize_image(encode_image('webpage_screenshot.png'), data_requirements)
        product_dict = json.loads((product_info.replace("'", '"')))
        product_dict["url"] = link
        output_product_list.append(product_dict)

    header_dict = {}
    data_requirements.append("url")
    headers = data_requirements
    header_dict["headers"] = headers
    header_dict["c"] = "c"
    header_dict["b"] = "b"
    header_dict["a"] = "a"
    output_product_list.insert(0, header_dict)

    print(output_product_list)

    # Respond back to the frontend
    return output_product_list

if __name__ == '__main__':
    app.run(debug=True)
