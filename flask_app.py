from flask import request, jsonify, Flask, g
from celery import Celery, chord
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

# Celery task to process URL
@celery.task
def process_data(url, keywords, task_id):

    result = process_url(url, keywords)
    
    if result:
        redis_conn.hset(f"results:{task_id}", url, json.dumps(result)) # Store the results using Redis
        print("URL PROCESSED:", result)

# Celery task to aggregate results
@celery.task
def aggregate_results(results, task_id=None, keywords=None):

    output_json = []
    all_results = redis_conn.hgetall(f"results:{task_id}")
    decoded_results = {key.decode('utf-8'): json.loads(value.decode('utf-8')) for key, value in all_results.items()}
    print(all_results)
    print(decoded_results)

    for url, result in decoded_results.items():
            print(type(result))
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

    redis_conn.set("my_key", json.dumps(output_json)) # Store aggregated result in Redis
    print("RESULTS AGGREGATED:", output_json)

# Flask route to receive POST and start tasks
@app.route('/receive_data', methods=['POST'])
def receive_data():
    data = request.get_json()
    task_id = str(uuid.uuid4())  # Generate unique task ID
    
    print("DATA RECEIVED:\n", data)
    link = data['siteUrl']
    tags = data['tags']
    keywords = data['dataRequirements']

    urls = product_search(tags, link)

    subtask_signatures = [process_data.s(url, keywords, task_id) for url in urls]  # Create processing tasks
    callback_signature = aggregate_results.s(task_id=task_id, keywords=keywords) # Create callback task
    chord(subtask_signatures)(callback_signature) # Process in parallel, then callback after all completed
    
    return jsonify({"task_id": task_id}), 202

@app.route('/reply_result', methods=['POST'])
def reply_result():
    
    results = redis_conn.get('my_key')

    if results:
        print("SENDING RESULTS:\n", results)
        return json.loads(results.decode('utf-8'))
    else:
        return jsonify({"message": "No result available."}), 202


if __name__ == '__main__':
    app.run(debug=True)

