from flask import request, jsonify, Flask, g
from celery import Celery, chord
from celery.signals import task_success
import os
import json
import redis
from multi import process_url
from pse import product_search
import uuid
from analyse import analyse_trend, analyse_price
from urllib.parse import urlparse

# Configure Redis settings
redis_url = urlparse(os.environ.get("REDIS_URL")) #+ '?ssl_cert_reqs=CERT_REQUIRED'
redis_conn = redis.Redis(host=redis_url.hostname, port=redis_url.port, password=redis_url.password, ssl=True, ssl_cert_reqs=None)

# Initialize Flask app
app = Flask(__name__)
app.json.sort_keys = False

# Configure Celery settings
app.config['CELERY_BROKER_URL'] = os.getenv('CLOUDAMQP_URL')
app.config['CELERY_RESULT_BACKEND'] = os.getenv("REDIS_URL")

# Initialize Celery
celery = Celery(__name__, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)  # Update Celery config with Flask app config



# Flask route to receive POST and start tasks
@app.route('/receive_data', methods=['POST'])
def receive_data():
    data = request.get_json()
    responseId = str(uuid.uuid4())  # Generate unique task ID
    
    print("DATA RECEIVED:\n" + str(data))
    link = data['siteUrl']
    tags = data['tags']
    # keywords = data['keywords']

    urls = product_search(tags, link)
    
    keywords = []
    if "lovebonito" in link:
        keywords.append("Price")
        keywords.append("Product Type")
        keywords.append("Color")
        keywords.append("Details")
    elif "pazzion" in link:
        keywords.append("Price")
        keywords.append("Product Type")
        keywords.append("Color")
        keywords.append("Description")

    subtask_signatures = [process_data.s(url, keywords, responseId) for url in urls]  # Create processing tasks
    callback_signature = aggregate_results.s(responseId=responseId, keywords=keywords) # Create callback task
    chord(subtask_signatures)(callback_signature) # Process in parallel, then callback after all completed
    
    return jsonify({"responseId": responseId}), 202



# Celery task to process URL
@celery.task
def process_data(url, keywords, responseId):

    result = process_url(url, keywords)
    
    if result:
        redis_conn.hset(f"results:{responseId}", url, result) # Store the results using Redis
        print("URL PROCESSED:" + str(result))



# Celery task to aggregate results
@celery.task
def aggregate_results(results, responseId, keywords):

    output_json = []
    all_results = redis_conn.hgetall(f"results:{responseId}")
    decoded_results = {key.decode('utf-8'): json.loads(value.decode('utf-8').replace("'", '"')) for key, value in all_results.items()}

    for url, result in decoded_results.items():
        result["url"] = url
        output_json.append(result) # Add a dictionary for each product

    #Add a dictionary containing analysis of entire dataset
    analysis_dict = {}
    price_dict = analyse_price(output_json)
    for price in price_dict:
        analysis_dict[price] = price_dict[price]
    analysis_dict["Trend"] = analyse_trend(output_json)
    output_json.insert(0, analysis_dict)

    # Add a dictionary containing necessary headers
    header_dict = {}
    keywords.append("url")
    header_dict["headers"] = keywords
    output_json.insert(1, header_dict)

    print("THIS IS THE RESPONSEID" + responseId)

    redis_conn.set("my_key", json.dumps(output_json)) # Store aggregated result in Redis
    print("RESULTS AGGREGATED:" + str(json.loads(redis_conn.get("my_key").decode('utf-8'))))



@app.route('/reply_result')
def reply_result():
    # responseId = request.args.get('responseId')
    # print("THIS IS THE RESPONSEID", responseId)
    
    # results = redis_conn.get(responseId)
    # print("THESE ARE THE RESULTS", json.loads(redis_conn.get(responseId).decode('utf-8')))

    results = redis_conn.get("my_key")

    if results:
        print("SENDING RESULTS:\n" + str(results))
        return json.loads(results.decode('utf-8'))
    else:
        print("NO RESULTS AVAILABLE")
        return jsonify({"status": "processing"}), 202  # Or use a different status/message as appropriate



if __name__ == '__main__':
    app.run(debug=True)

