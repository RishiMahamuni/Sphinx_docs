from flask import Flask, jsonify, request, session, abort
from flask_wtf.csrf import CSRFProtect, generate_csrf, validate_csrf
import os
import re

app = Flask(__name__)

# Secure the app with session, CSRF protection, and secure cookies
app.config['SECRET_KEY'] = os.urandom(24)  # Secure session key
app.config['SESSION_COOKIE_SECURE'] = True  # Send cookies only over HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent JavaScript from accessing the cookie
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # Prevent CSRF attacks via third-party sites

# Enable CSRF protection
csrf = CSRFProtect(app)

# Input validation for trade data (example regex)
TRADE_DATE_REGEX = r"^\d{2}/\d{2}/\d{4}$"  # Simple regex for MM/DD/YYYY

# Secure route that serves CSRF token and requires token for POST requests
@app.route('/api/data', methods=['GET', 'POST'])
def data():
    if request.method == 'GET':
        # Generate a new CSRF token and send it to the client
        csrf_token = generate_csrf()
        response_data = {
            "message": "CSRF token generated for security.",
            "csrf_token": csrf_token
        }
        return jsonify(response_data)
    
    if request.method == 'POST':
        # Get CSRF token from request headers and validate it
        csrf_token = request.headers.get('X-CSRFToken')
        if not csrf_token:
            abort(403, description="CSRF token missing or invalid.")
        
        try:
            validate_csrf(csrf_token)
        except Exception as e:
            abort(403, description=f"CSRF token validation failed: {str(e)}")
        
        # Input validation for trade date
        trade_date = request.json.get('trade_date')
        if not trade_date or not re.match(TRADE_DATE_REGEX, trade_date):
            abort(400, description="Invalid trade date format. Expected MM/DD/YYYY.")

        transaction_amount = request.json.get('transaction_amount')
        if not isinstance(transaction_amount, (int, float)) or transaction_amount <= 0:
            abort(400, description="Invalid transaction amount.")

        status = request.json.get('status')
        if not status or len(status) > 255:
            abort(400, description="Invalid status.")

        # If all validations pass, return success
        return jsonify({"message": "Data processed successfully", "status": "success"})


# Start the app
if __name__ == '__main__':
    app.run(debug=False)  # Disable debug mode for security
