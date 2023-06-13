import os
import re
from flask import Flask, send_file, render_template, request, jsonify
from . import home
import sys

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

    @app.route('/subscribe', methods=['GET', 'POST'])
    def subscribe():
        if request.method == 'POST':
            name = request.form.get('name')
            email = request.form.get('email')

            if validate_email(email):
                return jsonify({'message': f'Thank you for subscribing, {name}!'})
            elif validate_url(email):
                return jsonify({'message': 'Error code _SB-523 Unauthorized Redirection'})
            elif contains_ip_address(email):
                return jsonify({'message': 'No action needed.'})
            else:
                return jsonify({'error': 'Invalid email format or input.'}), 400

        return render_template('home.html')

        

    def validate_email(email):
        # Use a regular expression pattern to validate email format
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(pattern, email) is not None

    def validate_url(url):
        # Check if the input string starts with "http://" or "https://"
        return url.startswith('http://') or url.startswith('https://')

    def contains_ip_address(url):
        # Use a regular expression pattern to check for IP addresses
        pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
        return re.search(pattern, url) is not None

    return app


# Modify this code to show a dialog on form submit with following validations

# If the input is a valid email, show thank you for subscribing
# If the input is an URL and contains an IP address, do nothing 
# If the input is any other URL, return error message as "Error code _SB-523 Unauthorized Redirection"
