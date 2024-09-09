import requests

# Get data and CSRF token from the server
url = 'http://localhost:5000/api/data'
response = requests.get(url)
data = response.json()
csrf_token = data['csrf_token']

# Send POST request with CSRF token in the header
secure_url = 'http://localhost:5000/api/secure'
headers = {
    'X-CSRFToken': csrf_token  # Pass the CSRF token in the header
}

response = requests.post(secure_url, headers=headers)
print(response.json())
