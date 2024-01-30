from flask import Flask
from receive_data import app1 as app1_blueprint
from reply_result import app2 as app2_blueprint
from celery import Celery
import os

app = Flask(__name__)
app.json.sort_keys = False
app.register_blueprint(app1_blueprint)
app.register_blueprint(app2_blueprint)
app.config['CELERY_BROKER_URL'] = os.getenv('CLOUDAMQP_URL')  # Configure RabbitMQ broker
app.config['CELERY_RESULT_BACKEND'] = 'rpc://'  # Configure result backend

# Initialize Celery
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

if __name__ == "__main__":
    app.run()
