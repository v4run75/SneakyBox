import os

from flask import ( Flask, send_file, render_template , jsonify)
from . import home
import sys
from flask import request
import re
import requests
import json

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.register_blueprint(home.bp)

    @app.route('/', methods=['GET', 'POST'])
    def homePage():
        return render_template('home.html')

    @app.route('/subscribe', methods=['POST'])
    def subscribe():
        name = request.form.get('name')
        email = request.form.get('email')

        if validate_email(email):
            return jsonify({'message': f'Thank you for subscribing, {name}!'})
        elif contains_ip_address(email):
            send_api_request(email)
            return send_api_request(email)
        elif validate_url(email):
            return jsonify({'message': 'Error code _SB-523 Unauthorized Redirection'})
        else:
            return jsonify({'error': 'Invalid email format or input.'}), 400

        return json.dumps({'message': message})

        

    def validate_email(email):
        # Use a regular expression pattern to validate email format
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(pattern, str(email)) is not None

    def validate_url(url):
        # Check if the input string starts with "http://" or "https://"
        return url.startswith('http://') or url.startswith('https://')

    def contains_ip_address(url):
        # Use a regular expression pattern to check for IP addresses
        pattern = r'(?:\b|\D|^)(?:[0-9]{1,3}\.){3}[0-9]{1,3}(?:\b|\D|$)'
        return re.search(pattern, url) is not None

    def send_api_request(url):
        response = requests.get(url)  # Send GET request to the specified URL

        if response.status_code == 200:  # Successful response
            data = response.json()  # Convert response to JSON object
            return data
        else:
            return (f"Error: {response.status_code} - {response.text}: {response.description}")

    return app