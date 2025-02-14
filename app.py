import logging
from flask import Flask, render_template, request, jsonify,redirect, url_for,flash
import datetime
from getmac import get_mac_address
from flask_mail import Mail, Message
from flask_socketio import SocketIO, emit
import random
app = Flask(__name__)

# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Use your email provider's SMTP server
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'hezynavy@gmail.com'  # Replace with your email
app.config['MAIL_PASSWORD'] = 'omondi7ns'  # Replace with your password
app.config['MAIL_DEFAULT_SENDER'] = 'hezynavy@gmail.com'

mail = Mail(app)

@app.route('/support', methods=['POST'])
def send_support_email():
    name = request.form.get('name')
    email = request.form.get('email')  # User's email
    issue = request.form.get('issue')

    if not name or not email or not issue:
        flash("All fields are required!", "error")
        return redirect(url_for('support'))

    # Validate email format
    if "@" not in email or "." not in email:
        flash("Invalid email format!", "error")
        return redirect(url_for('support'))

    # Fixed support email
    support_email = "support@echotelecom.com"

    # Send email to support team
    support_msg = Message("New Support Request", recipients=[support_email])
    support_msg.body = f"Name: {name}\nEmail: {email}\nIssue: {issue}"
    mail.send(support_msg)

    # Auto-reply to user
    user_msg = Message("Support Request Received", recipients=[email])
    user_msg.body = f"Hi {name},\n\nWe've received your support request:\n\n{issue}\n\nOur team will get back to you soon!"
    mail.send(user_msg)

    flash("Your message has been sent successfully!", "success")
    return redirect(url_for('support'))
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
# Simulated Database
paid_users = {}

@app.route('/check_hotspot', methods=['GET'])
def check_hotspot():
    # Simulate checking hotspot status
    hotspot_available = True
    return jsonify({'available': hotspot_available})
@app.route('/process_payment', methods=['POST'])
def process_payment():
    data = request.json
    pin = data.get("pin")
    speed = data.get("speed")
    price = data.get("price")
    device_mac = data.get("mac_address")  # Get MAC address

    if pin == "1234":  # Example correct PIN
        expiration_time = datetime.datetime.now() + datetime.timedelta(days=30)  # 30 days subscription
        paid_users[device_mac] = {"speed": speed, "expires_at": expiration_time}

        return jsonify({"success": True, "message": "Payment successful! Subscription active."})
    else:
        return jsonify({"success": False, "message": "Invalid PIN."})

@app.route('/check_access', methods=['POST'])
def check_access():
    ip_address = request.remote_addr
    device_mac = get_mac_address(ip=ip_address)

    if device_mac and device_mac in paid_users:
        return jsonify({'access': 'granted', 'speed': paid_users[device_mac]['speed']})

    return jsonify({'access': 'denied', 'message': 'Payment required.'})

@app.route('/connect_wifi')
def connect_wifi():
    device_mac = request.args.get("mac")

    if device_mac in paid_users:
        subscription = paid_users[device_mac]
        current_time = datetime.datetime.now()

        if current_time < subscription["expires_at"]:
            return redirect("https://your_wifi_network")  # Allow connection
        else:
            del paid_users[device_mac]  # Remove expired subscription
            return redirect(url_for("packages"))  # Redirect to renew subscription

    return redirect(url_for("packages")) 
@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    # Process search logic here
    return render_template('search_results.html', query=query)
socketio = SocketIO(app, cors_allowed_origins="*")

# Simple chatbot responses
responses = {
    "hello": ["Hi there!", "Hello!", "Hey!"],
    "help": ["How can I assist you?", "What do you need help with?"],
    "price": ["Our prices are competitive. Contact sales for details."],
    "bye": ["Goodbye!", "Have a great day!", "See you later!"],
}

support_agents = set()  # Track online support agents

@app.route('/')
def index():
    return render_template('contact.html')

@socketio.on('user_message')
def handle_user_message(data):
    user_message = data['message'].lower()

    # Check if user needs human support
    if "help" in user_message or "support" in user_message:
        notify_support(user_message)
        emit('bot_response', {'response': "A support agent will join shortly."})
    else:
        bot_reply = random.choice(responses.get(user_message, ["I'm not sure. Can you rephrase?"]))
        emit('bot_response', {'response': bot_reply})

def notify_support(message):
    """Notify all online support agents that a user needs help."""
    if support_agents:
        for agent in support_agents:
            socketio.emit('support_response', {'response': f"User needs help: {message}"}, room=agent)

@socketio.on('support_join')
def support_join():
    """A support agent joins the chat."""
    support_agents.add(request.sid)
    emit('support_response', {'response': "Support agent is online."})

@socketio.on('support_message')
def support_message(data):
    """Forward support agent message to the user."""
    emit('support_response', {'response': data['message']}, broadcast=True)

if __name__ == '__main__':
    app.run(debug=True)
