from flask import request, jsonify, Flask, g
from celery import Celery, chord
import os
import json
import redis
from multi import process_url
from seo import product_search
import uuid

redis_conn = redis.from_url(os.getenv("REDIS_URL"))

# Initialize Flask app
app = Flask(__name__)
app.json.sort_keys = False

# Configure Celery settings
app.config['CELERY_BROKER_URL'] = os.getenv('CLOUDAMQP_URL')
app.config['CELERY_RESULT_BACKEND'] = os.getenv('CLOUDAMQP_URL')

# Initialize Celery
celery = Celery(__name__, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)  # Update Celery config with Flask app config

# Celery task to process URL
@celery.task
def process_url(url, keywords, task_id):

    result = process_url(url, keywords)

    redis_conn.hset(f"results:{task_id}", url, json.dumps(result)) # Store the results using Redis
    print("URL PROCESSED:", result)

# Celery task to aggregate results
@celery.task
def aggregate_results(task_id):
    all_results = redis_conn.hgetall(f"results:{task_id}")
    aggregated_result = {url: json.loads(result.decode('utf-8')) for url, result in all_results.items()}

    redis_conn.set("my_key", json.dumps(aggregated_result))  # Store aggregated result in Redis
    print("RESULTS AGGREGATED:", aggregated_result)

# Flask route to receive POST and start tasks
@app.route('/receive_data', methods=['POST'])
def receive_data():
    data = request.get_json() # Get JSON data sent from the frontend
    task_id = str(uuid.uuid4())  # Generate unique task ID
    
    # Log or process the data here
    print("DATA RECEIVED:\n", data)
    link = data['siteUrl']
    tags = data['tags']
    keywords = data['dataRequirements']

    urls = product_search(tags, link)

    subtask_signatures = [process_url.s(url, keywords, task_id) for url in urls] 
    chord(subtask_signatures)(aggregate_results.s(task_id=task_id))  # Run tasks in parallel
    
    return jsonify({"task_id": task_id}), 202

@app.route('/reply_result', methods=['POST'])
def reply_result():
    
    results = redis_conn.get('my_key')

    if results:
        print("SENDING RESULTS:\n", results)
        return json.loads(results.decode('utf-8'))  # Decode from bytes to string
    else:
        return jsonify({"message": "No result available."}), 202


if __name__ == '__main__':
    app.run(debug=True)

