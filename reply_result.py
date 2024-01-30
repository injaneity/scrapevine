from receive_data import output_json
from flask import Flask

app2 = Flask(__name__)
app2.json.sort_keys = False

@app2.route('/reply_result', methods=['POST'])
def reply_result():
    print(output_json)
    return output_json

if __name__ == '__main__':
    app2.run(debug=True)