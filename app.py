from flask import Flask, request, jsonify
from celery import Celery
from celery_task import process_data

app = Flask(__name__)
app.json.sort_keys = False
app.config['CELERY_BROKER_URL'] = 'amqps://keyribfx:GnjDeFVk12DsXeKrGtq746M2_jtIsMjd@moose.rmq.cloudamqp.com/keyribfx'  # Configure RabbitMQ broker
app.config['CELERY_RESULT_BACKEND'] = 'rpc://'  # Configure result backend

# Initialize Celery
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

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

if __name__ == '__main__':
    app.run(debug=True)
