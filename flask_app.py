from flask import request, jsonify, Flask, g
from celery import Celery
import os
import json
import redis

output_json1 = [
    {
        "Average Price": "32.93",
        "Highest Price": "49.90",
        "Lowest Price": "19.00",
        "Trend": "Brief Analysis: The provided data showcases a small selection of clothing products, specifically dresses, with varying prices and colors. The price range spans from $19.00 to $49.90, indicating a market that caters to mid-range budget consumers. The types of dresses include a Square Neck Knit Dress, a Shirt Dress, and a general Dress category, suggesting a variety in styles that could appeal to different consumer preferences. The colors represented are Black, Lime, and White, which shows a mix of both classic (Black and White) and more vibrant, trendy options (Lime). This diversity in color and style could indicate a market that values both timeless pieces and seasonal trends. For businesspeople looking to enter this market, focusing on offering a variety of dress styles at a mid-range price point could be a strategic approach. Additionally, incorporating both classic colors and a selection of trend-driven hues might cater to a broader customer base. The presence of knit and ruffle details suggests that texture and fabric choice could also be significant factors for consumers in this market."
    },
    {
        "headers": [
            "Price",
            "Product Type",
            "Color",
            "url"
        ]
    },
    {
        "Price": "19.00",
        "Product Type": "Square Neck Knit Dress",
        "Color": "Black",
        "url": "https://www.lovebonito.com/sg/abilene-square-neck-knit-dress.html"
    },
    {
        "Price": "29.90",
        "Product Type": "Shirt Dress",
        "Color": "Lime",
        "url": "https://www.lovebonito.com/sg/anniston-puff-sleeve-shirt-dress.html"
    },
    {
        "Price": "49.90",
        "Product Type": "Dress",
        "Color": "White",
        "url": "https://www.lovebonito.com/sg/dacia-drop-waist-ruffle-dress.html"
    }
]

redis_conn = redis.from_url(os.getenv("REDIS_URL"))

app = Flask(__name__)
app.json.sort_keys = False

celery = Celery(__name__)
# Configure Celery settings
app.config['CELERY_BROKER_URL'] = os.getenv('CLOUDAMQP_URL')
app.config['CELERY_RESULT_BACKEND'] = 'rpc://'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

from pse import product_search
from gpt_functions import encode_image, summarize_image, analyse_trend
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from price_analysis import analyse_price

@celery.task
def process_data(url, tags, data_requirements):

    input_product_list = product_search(tags, url)

    output_product_list = []

    if not input_product_list:
        print("Empty product list")
        
    else:
        # Initialize a Chrome session
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # Run in headless mode, no UI is displayed
        options.add_argument("--disable-gpu")  # Necessary for some versions of Chrome
        options.add_argument("--no-sandbox")  # Bypass OS security model, required on Heroku
        options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
        options.add_argument("--window-size=1536,1536")  # Set appropriate window size
        options.add_argument("--force-device-scale-factor=1.1")  # Zoom in by 110%
        options.add_argument("--hide-scrollbars")  # Hide scrollbars to avoid them appearing in screenshots
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36")
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.set_page_load_timeout(30)

        for link in input_product_list:

            # Open the webpage
            driver.get(link)
            time.sleep(3)

            # Save the screenshot as a PNG file to the project folder
            driver.save_screenshot("webpage_screenshot.png")

            product_info = summarize_image(encode_image('webpage_screenshot.png'), data_requirements)
            product_dict = json.loads((product_info.replace("'", '"')))

            # Check for empty strings
            keys_not_empty = all(key != '' for key in product_dict.keys())
            values_not_empty = all(value != '' for value in product_dict.values())

            # Check if all conditions are met
            if keys_not_empty and values_not_empty and product_dict != {}:
                product_dict["url"] = link
                output_product_list.append(product_dict)
        
        # Close the browser
        driver.quit()
    
        analysis_dict = {}
        price_dict = analyse_price(output_product_list)

        for price in price_dict:
            analysis_dict[price] = price_dict[price]

        analysis_dict["Trend"] = analyse_trend(output_product_list)

        output_product_list.insert(0, analysis_dict)

    header_dict = {}
    data_requirements.append("url")
    headers = data_requirements
    header_dict["headers"] = headers

    output_product_list.insert(1, header_dict)
 
    # with open("output.json", "w") as json_file:
    #     json.dump(output_product_list, json_file)

    redis_conn.set('my_key', json.dumps(output_json1))
    print("This is output JSON", output_json1)

@app.route('/receive_data', methods=['POST'])
def receive_data():
    # Get JSON data sent from the frontend
    data = request.get_json()
    
    # Log or process the data here
    print("Data received:", data)

    url = data['siteUrl']
    tags = data['tags']
    data_requirements = data['dataRequirements']

    task = process_data.delay(url, tags, data_requirements)  # Sending the task to the queue
    return jsonify({"task_id": task.id}), 202

@app.route('/reply_result', methods=['POST'])
def reply_result():
    # if os.path.exists("output.json") and os.path.getsize("output.json") > 0:
    #     with open("output.json", "r") as json_file:
    #         output_json = json.load(json_file)
    #         return output_json
    # else:
    #     print("No JSON file.")
    #     return jsonify({"message": "No data available"}), 404
    
    output_json = redis_conn.get('my_key')
    print("This is output JSON again", output_json)

    if output_json:
        return json.loads(output_json.decode('utf-8'))  # Decode from bytes to string
    else:
        return jsonify({"message": "No data available"}), 202


if __name__ == '__main__':
    app.run(debug=True)

