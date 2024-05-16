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
redis_url = urlparse(os.environ.get("REDIS_URL"))
redis_conn = redis.Redis(host=redis_url.hostname, port=redis_url.port, password=redis_url.password, ssl=True, ssl_cert_reqs=None)

# Initialize Flask app
app = Flask(__name__)
app.json.sort_keys = False

# Initialize Celery
celery = Celery(__name__, backend=os.getenv("REDIS_URL") + '?ssl_cert_reqs=CERT_NONE', broker=os.getenv('CLOUDAMQP_URL'))



# Flask route to receive POST and start tasks
@app.route('/receive_data', methods=['POST'])
def receive_data():
    data = request.get_json()
    responseId = str(uuid.uuid4())  # Generate unique task ID
    
    print("DATA RECEIVED:\n" + str(data))
    link = data['siteUrl']
    rawtags = data['tags']
    # keywords = data['keywords']

    # Transform tags into a list of individual words
    tags = []
    for tag in rawtags:
        tags.extend(tag.split())
    print(tags)

    urls = product_search(tags, link)
    
    # Dictionary mapping site keywords to their respective keywords
    keyword_map = {
        "lovebonito": ["Price", "Product Type", "Color", "Details"],
        "pazzion": ["Price", "Product Type", "Color", "Description"]
    }
    
    # Determine the appropriate keywords based on the link
    keywords = []
    for site, site_keywords in keyword_map.items():
        if site in link.lower():
            keywords = site_keywords
            break

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
        print("URL PROCESSED:\n" + str(result))



# Celery task to aggregate results
@celery.task
def aggregate_results(results, responseId, keywords):

    output_json = []
    all_results = redis_conn.hgetall(f"results:{responseId}")
    decoded_results = {key.decode('utf-8'): json.loads(value.decode('utf-8').replace("'", '"')) for key, value in all_results.items()}

    for url, result in decoded_results.items():
        # Check if any value in the result dictionary is not an empty string
        if all(value == '' for value in result.values()):
            print("BAD LINK: " + url)
        else:
            result["URL"] = url
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
    keywords.append("URL")
    header_dict["headers"] = keywords
    output_json.insert(1, header_dict)

    #print("THIS IS THE RESPONSEID" + responseId)

    redis_conn.set("my_key", json.dumps(output_json)) # Store aggregated result in Redis
    print("RESULTS AGGREGATED:\n" + str(json.loads(redis_conn.get("my_key").decode('utf-8'))))



@app.route('/reply_result')
def reply_result():
    # responseId = request.args.get('responseId')
    # print("THIS IS THE RESPONSEID", responseId)
    
    # results = redis_conn.get(responseId)
    # print("THESE ARE THE RESULTS", json.loads(redis_conn.get(responseId).decode('utf-8')))

    results = redis_conn.get("my_key")

    if results:
        print("SENDING RESULTS:\n" + str(results))
        redis_conn.delete("my_key")
        return json.loads(results.decode('utf-8'))
    else:
        print("NO RESULTS AVAILABLE")
        return jsonify({"status": "processing"}), 202  # Or use a different status/message as appropriate



if __name__ == '__main__':
    app.run(debug=True)

