from flask import request, jsonify, Flask, g
from celery import Celery, chord
from celery.signals import task_success
import os
import json
import re
import redis
from multi import process_url
from pse import product_search
import uuid
from analyse import analyse_trend, analyse_price
from urllib.parse import urlparse



# Load keyword map from JSON file
with open('map.json', 'r') as f:
    map = json.load(f)

# Configure Redis settings
redis_url = urlparse(os.environ.get("REDIS_URL"))
redis_conn = redis.Redis(host=redis_url.hostname, port=redis_url.port, password=redis_url.password, ssl=True, ssl_cert_reqs=None)

# Initialize Flask app
app = Flask(__name__)
app.json.sort_keys = False

# Initialize Celery
celery = Celery(__name__, backend=os.getenv("REDIS_URL") + '?ssl_cert_reqs=CERT_NONE', broker=os.getenv('CLOUDAMQP_URL'))
celery.conf.update(
    worker_concurrency=1,  # Ensure each worker handles one task at a time
    task_acks_late=True,  # Ensure tasks are acknowledged after completion
    worker_prefetch_multiplier=1  # Prevent multiple tasks from being assigned to the same worker
)



# Function to scale dynos
def scale_dynos(dyno_type, quantity):
    url = f"https://api.heroku.com/apps/{os.getenv('HEROKU_APP_NAME')}/formation/{dyno_type}"
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/vnd.heroku+json; version=3',
        'Authorization': f'Bearer {os.getenv('HEROKU_API_KEY')}'
    }
    data = {
        "quantity": quantity
    }
    response = requests.patch(url, headers=headers, json=data)
    if response.status_code == 200:
        print(f"SCALED {dyno_type} DYNOS TO {quantity}")
    else:
        print(f"FAILED TO SCALE DYNOS: {response.content}")



# Flask route to receive user input
@app.route('/receive_data', methods=['POST'])
def receive_data():
    # Scale up dynos
    scale_dynos('worker', 5)

    data = request.get_json()
    responseId = str(uuid.uuid4())  # Generate unique task ID
    
    print("DATA RECEIVED:\n" + str(data))
    rawlink = data['siteUrl']
    rawtags = data['tags']

    # Transform rawtags string into a list of individual words
    tags = re.split(r'[^a-zA-Z]+', rawtags)
    # Filter out any empty strings that may result from splitting
    tags = list(filter(None, tags))
    print(tags)
    
    # Determine the appropriate keywords based on the link
    keywords = []
    link = None
    match_found = False
    for site, site_data in map.items():
        if site in rawlink.lower():
            link = site_data["link"]  # Update link to the one in map
            keywords = site_data["keywords"]
            match_found = True
            break

    if not match_found:
        print(f"NO MATCHING WEBSITE FOR {rawlink}")
        return jsonify({"error": f"NO MATCHING WEBSITE FOR {rawlink}"}), 400

    urls = product_search(tags, link)

    subtask_signatures = [process_data.s(url, keywords, responseId) for url in urls]  # Create processing tasks
    callback_signature = aggregate_results.s(responseId=responseId, keywords=keywords) # Create callback task
    chord(subtask_signatures)(callback_signature) # Process in parallel, then callback after all completed
    
    return jsonify({"responseId": responseId}), 202



# Celery task to process URL
@celery.task
def process_data(url, keywords, responseId):

    result = process_url(url, keywords)
    
    if result:
        redis_conn.hset(f"results:{responseId}", url, result) # Store the results using Redis
        print("URL PROCESSED:\n" + str(result))



# Celery task to aggregate results
@celery.task
def aggregate_results(results, responseId, keywords):

    output_json = []
    all_results = redis_conn.hgetall(f"results:{responseId}")
    decoded_results = {key.decode('utf-8'): json.loads(value.decode('utf-8').replace("'", '"')) for key, value in all_results.items()}

    for url, result in decoded_results.items():
        # Check if any value in the result dictionary is not an empty string
        if all(value == '' for value in result.values()):
            print("BAD LINK: " + url)
        else:
            result["URL"] = url
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
    keywords.append("URL")
    header_dict["headers"] = keywords
    output_json.insert(1, header_dict)

    #print("THIS IS THE RESPONSEID" + responseId)

    redis_conn.set("my_key", json.dumps(output_json)) # Store aggregated result in Redis
    print("RESULTS AGGREGATED:\n" + str(json.loads(redis_conn.get("my_key").decode('utf-8'))))

    # Scale down dynos after tasks complete
    scale_dynos('worker', 0)



# Flask route to reply with results
@app.route('/reply_result', methods=['GET'])
def reply_result():
    # responseId = request.args.get('responseId')
    # print("THIS IS THE RESPONSEID", responseId)
    
    # results = redis_conn.get(responseId)
    # print("THESE ARE THE RESULTS", json.loads(redis_conn.get(responseId).decode('utf-8')))

    results = redis_conn.get("my_key")

    if results:
        print("SENDING RESULTS:\n" + str(results))
        redis_conn.delete("my_key")
        return json.loads(results.decode('utf-8'))
    else:
        print("NO RESULTS AVAILABLE")
        return jsonify({"status": "processing"}), 202  # Or use a different status/message as appropriate



if __name__ == '__main__':
    app.run(debug=True)

