from flask import request, jsonify, Blueprint
from celery_task import process_data

output_json = {}

app1 = Blueprint("app1", __name__)

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


