from flask import Flask, request, jsonify

app = Flask(__name__)

def send_data():

@app.route('/receive_data', methods=['POST'])
def receive_data():
    # Get JSON data sent from the frontend
    data = request.get_json()
    
    # Log or process the data here
    print("Received data:", data)

    sample_data = [
        {"headers": ["name", "colour", "price", "url"]},
        {"name": "Sport Running Shoes", "colour": "White", "price": "$89", "url": "https://example.com/product/sport-running-shoes"},
        {"name": "Smartphone X200", "colour": "Black", "price": "$299", "url": "https://example.com/product/smartphone-x200"},
        {"name": "Bluetooth Headphones E7", "colour": "Red", "price": "$79", "url": "https://example.com/product/bluetooth-headphones-e7"},
        {"name": "Leather Wallet Classic", "colour": "Brown", "price": "$35", "url": "https://example.com/product/leather-wallet-classic"},
        {"name": "Summer Dress Floral", "colour": "Blue", "price": "$49", "url": "https://example.com/product/summer-dress-floral"}
    ]

    # Respond back to the frontend with the sample JSON data
    return jsonify(sample_data)



if __name__ == '__main__':
    app.run()
