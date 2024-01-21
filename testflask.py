from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/receive_data', methods=['POST'])
def receive_data():
    # Get JSON data sent from the frontend
    data = request.get_json()
    
    # Log or process the data here
    print("Received data:", data)

    # Respond back to the frontend
    return jsonify({'status': 'success', 'message': 'Data received'})

if __name__ == '__main__':
    app.run()
