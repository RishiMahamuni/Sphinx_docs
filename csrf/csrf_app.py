from flask import Flask, jsonify, request, session
from flask_wtf.csrf import CSRFProtect, generate_csrf
import os

app = Flask(__name__)

# Secret key for session management and CSRF token generation
app.config['SECRET_KEY'] = os.urandom(24)

# Enable CSRF protection
csrf = CSRFProtect(app)

# Route to return JSON data and dynamically generated CSRF token
@app.route('/api/data', methods=['GET', 'POST'])
def data():
    # Generate a new CSRF token for each request
    csrf_token = generate_csrf()

    # Return data along with the CSRF token in the response
    data = {
        "trade_date": "03/05/2020",
        "transaction_amount": 1500.50,
        "status": "Completed",
        "csrf_token": csrf_token  # Include CSRF token in response
    }
    
    return jsonify(data)

# Protected route that requires a valid CSRF token in the headers
@app.route('/api/secure', methods=['POST'])
@csrf.exempt  # We can also skip this in case of API (by default)
def secure_data():
    # CSRF token will be validated automatically by Flask-WTF
    return jsonify({"message": "Secure data accessed!"})

if __name__ == '__main__':
    app.run(debug=True)
