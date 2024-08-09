from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields
import requests

# Create a Flask application
app = Flask(__name__)
api = Api(app, version='1.0', title='Rasa API',
          description='A simple Rasa-enabled API')

# Define the request model for Swagger
message_model = api.model('Message', {
    'message': fields.String(required=True, description='Message to send to Rasa'),
})

# Endpoint to interact with the Rasa API
@api.route('/rasa/message')
class RasaMessage(Resource):
    @api.expect(message_model)
    def post(self):
        """Send a message to the Rasa API and receive a response"""
        # Get the JSON data from the request
        data = request.json
        user_message = data['message']

        # Define the Rasa endpoint URL
        rasa_url = 'http://localhost:5005/webhooks/rest/webhook'

        # Send the message to the Rasa API
        response = requests.post(rasa_url, json={'message': user_message})

        # Return the Rasa API response
        if response.ok:
            return jsonify(response.json())
        else:
            return {'error': 'Failed to connect to Rasa API'}, 500

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
