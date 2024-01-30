from flask_app import celery  # Import Celery instance from your main app module

if __name__ == '__main__':
    celery.worker_main()