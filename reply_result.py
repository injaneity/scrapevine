from receive_data import output_json
from flask import Blueprint

app2 = Blueprint("app2", __name__)
app2.json.sort_keys = False

@app2.route('/reply_result', methods=['POST'])
def reply_result():
    print(output_json)
    return output_json