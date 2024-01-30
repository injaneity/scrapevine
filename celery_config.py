from celery import Celery
import os

# Create a shared Celery instance
celery = Celery(__name__)

# Configure Celery
celery.conf.update(
    broker_url=os.getenv('CLOUDAMQP_URL'),  # Use your preferred broker URL
    result_backend='rpc://',  # Use your preferred result backend URL
    # Add any other Celery configuration options here
)
