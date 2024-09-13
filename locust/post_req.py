import json
import requests

def load_json(file_path):
    """Load data from a JSON file."""
    with open(file_path, 'r') as file:
        return json.load(file)

def make_post_request(api_url, payload):
    """Make a POST request to the API endpoint with the given payload."""
    try:
        response = requests.post(api_url, json=payload)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)
        return response
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None

def main():
    # Define file paths
    config_path = "config.json"
    payload_path = "payload.json"

    # Load configuration and payload
    config = load_json(config_path)
    payload = load_json(payload_path)

    # Get API URL from config
    api_url = config.get("endpoint")
    if not api_url:
        print("API endpoint not found in the config file.")
        return

    # Make the POST request
    response = make_post_request(api_url, payload)
    if response:
        print(f"Response Status Code: {response.status_code}")
        print(f"Response Body: {response.text}")

if __name__ == "__main__":
    main()
