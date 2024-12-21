from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/products')
def products():
    return render_template('products.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')
@app.route('/community')
def community():
    return render_template('community.html')
@app.route('/projects')
def projects():
    return render_template('projects.html')
@app.route('/support')
def support():
    return render_template('Support.html')
@app.route('/explore')
def explore():
    return render_template('Explore.html')

@app.route('/services')
def services():
    subscriptions = {
        "6Mbps": "1500",
        "8Mbps": "1850",
        "10Mbps": "2000",
        "15Mbps": "2800",
        "30Mbps": "3800",
        "40Mbps": "4500",
        "60Mbps": "6000",
        "80Mbps": "7000",
        "90Mbps": "8000",
        "100Mbps": "10000"
    }
    return render_template('services.html', subscriptions=subscriptions)

@app.route('/process_payment', methods=['POST'])
def process_payment():
    pin = request.form['pin']
    speed = request.form['speed']
    price = request.form['price']

    # Simulate PIN validation
    if pin == '1234':  # Example PIN validation
        return jsonify({"message": f"Payment successful for {speed} at {price} KSH. Your WiFi subscription is now active!", "success": True})
    else:
        return jsonify({"message": "Invalid PIN. Payment failed.", "success": False}), 400

if __name__ == '__main__':
    app.run(debug=True)
