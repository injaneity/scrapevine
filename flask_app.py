from flask import request, jsonify, Flask, g
from celery import Celery
import os
import json
import redis
from multi import main

redis_conn = redis.from_url(os.getenv("REDIS_URL"))

# Initialize Flask app
app = Flask(__name__)
app.json.sort_keys = False

# Configure Celery settings
app.config['CELERY_BROKER_URL'] = os.getenv('CLOUDAMQP_URL')
app.config['CELERY_RESULT_BACKEND'] = 'rpc://'

# Initialize Celery
celery = Celery(__name__, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)  # Update Celery config with Flask app config

@celery.task
def process_data(url, tags, keywords):

    results = main(url, tags, keywords)

    redis_conn.set('my_key', json.dumps(results)) # Store the results using redis
    print("DATA HAS BEEN PROCESSED:", results)

@app.route('/receive_data', methods=['POST'])
def receive_data():
    # Get JSON data sent from the frontend
    data = request.get_json()
    
    # Log or process the data here
    print("DATA RECEIVED FROM FRONTEND:\n", data)

    url = data['siteUrl']
    tags = data['tags']
    keywords = data['dataRequirements']

    task = process_data.delay(url, tags, keywords)  # Sending the task to the queue
    return jsonify({"message": "Data is being processed."}), 202

@app.route('/reply_result', methods=['POST'])
def reply_result():
    
    results = redis_conn.get('my_key')

    if results:
        print("SENDING RESULT TO FRONTEND:\n", results)
        return json.loads(results.decode('utf-8'))  # Decode from bytes to string
    else:
        return jsonify({"message": "No data available."}), 202


if __name__ == '__main__':
    app.run(debug=True)

