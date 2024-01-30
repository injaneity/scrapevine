from flask import request, jsonify, Blueprint
from celery import Celery
import os

output_json = {}

app1 = Blueprint("app1", __name__)
app1.config['CELERY_BROKER_URL'] = os.getenv('CLOUDAMQP_URL')  # Configure RabbitMQ broker
app1.config['CELERY_RESULT_BACKEND'] = 'rpc://'  # Configure result backend

# Initialize Celery
celery = Celery(app1.name, broker=app1.config['CELERY_BROKER_URL'])
celery.conf.update(app1.config)

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

    if input_product_list == []:
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
            if product_dict != {}:
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

    global output_json
    output_json = output_product_list
    print(output_json)

@app1.route('/receive_data', methods=['POST'])
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


