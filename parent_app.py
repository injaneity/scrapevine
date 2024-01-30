from flask import Flask
from receive_data import app1 as app1_blueprint
from reply_result import app2 as app2_blueprint
from celery_config import celery

app = Flask(__name__)
app.json.sort_keys = False
app.register_blueprint(app1_blueprint)
app.register_blueprint(app2_blueprint)

# Initialize Celery for app1_blueprint
celery.init_app(app1_blueprint)

# Initialize Celery for app2_blueprint
celery.init_app(app2_blueprint)

if __name__ == "__main__":
    app.run()
