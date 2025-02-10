import logging
from flask import Flask, render_template, request, jsonify

app = Flask(__name__, static_folder='static', template_folder='templates')

logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def home():
    return render_template('index.html')

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
    return render_template('support.html')  # Fix capitalization

@app.route('/explore')
def explore():
    return render_template('explore.html')  # Fix capitalization

@app.route('/careers')
def careers():
    return render_template('careers.html')

@app.route('/blog')
def blog():  # Fix function name capitalization
    return render_template('Blog.html')

@app.route('/packages')
def packages():
    subscriptions = {
        "6Mbps": "1500",
        "8Mbps": "1850",
        "10Mbps": "2000",
        "15Mbps": "2500",
        "30Mbps": "3500",
        "40Mbps": "4500",
        "60Mbps": "6000",
        "80Mbps": "7500",
        "90Mbps": "8500",
        "100Mbps": "10000"
    }
    return render_template('packages.html', subscriptions=subscriptions)

@app.route('/process_payment', methods=['POST'])
def process_payment():
    try:
        pin = request.form['pin']
        speed = request.form['speed']
        price = request.form['price']

        if pin == '1234':  
            return jsonify({"message": f"Payment successful for {speed} at {price} KSH. Your WiFi subscription is now active!", "success": True})
        else:
            return jsonify({"message": "Invalid PIN. Payment failed.", "success": False}), 400
    except Exception as e:
        app.logger.error(f"Error processing payment: {e}")
        return jsonify({"message": "Internal server error", "success": False}), 500

if __name__ == '__main__':
    app.run(debug=True)
