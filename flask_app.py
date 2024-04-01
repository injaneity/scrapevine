from flask import request, jsonify, Flask, g
from celery import Celery, chord
from celery.signals import task_success
import os
import json
import redis
from multi import process_url
from seo import product_search
import uuid
from analyse import analyse_trend, analyse_price

# Configure Redis settings
redis_conn = redis.from_url(os.getenv("REDIS_URL"))

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
    task_id = str(uuid.uuid4())  # Generate unique task ID
    
    print("DATA RECEIVED:\n", data)
    link = data['siteUrl']
    tags = data['tags']
    keywords = data['keywords']

    urls = product_search(tags, link)

    subtask_signatures = [process_data.s(url, keywords, task_id) for url in urls]  # Create processing tasks
    callback_signature = aggregate_results.s(task_id=task_id, keywords=keywords) # Create callback task
    chord(subtask_signatures)(callback_signature) # Process in parallel, then callback after all completed
    
    return jsonify({"task_id": task_id}), 202



# Celery task to process URL
@celery.task
def process_data(url, keywords, task_id):

    result = process_url(url, keywords)
    
    if result:
        redis_conn.hset(f"results:{task_id}", url, result) # Store the results using Redis
        print("URL PROCESSED:", result)



# Celery task to aggregate results
@celery.task
def aggregate_results(results, task_id=None, keywords=None):

    output_json = []
    all_results = redis_conn.hgetall(f"results:{task_id}")
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

    redis_conn.set(f"aggregated_results:{task_id}", json.dumps(output_json)) # Store aggregated result in Redis
    print("RESULTS AGGREGATED:", json.loads(redis_conn.get(f"aggregated_results:{task_id}").decode('utf-8')))



@app.route('/reply_result')
def reply_result():
    task_id = request.args.get('responseId')
    
    results = redis_conn.get(f"aggregated_results:{task_id}")

    if results:
        print("SENDING RESULTS:\n", results)
        return json.loads(results.decode('utf-8'))
    else:
        print("NO RESULTS AVAILABLE")
        return jsonify({"status": "processing"}), 202  # Or use a different status/message as appropriate



if __name__ == '__main__':
    app.run(debug=True)

