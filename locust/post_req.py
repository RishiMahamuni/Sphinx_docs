import json
import requests
import time
from tqdm import tqdm

def load_json(file_path):
    """Load data from a JSON file."""
    with open(file_path, 'r') as file:
        return json.load(file)

def make_post_request(api_url, payload):
    """Make a POST request to the API endpoint with the given payload and show progress and timing."""
    try:
        print("Sending POST request...")
        
        # Start the timer
        start_time = time.time()

        # Create a progress bar with tqdm
        with tqdm(total=1, desc="Request Progress") as pbar:
            response = requests.post(api_url, json=payload)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)
            # Update progress bar
            pbar.update(1)

        # End the timer
        end_time = time.time()
        duration = end_time - start_time

        print(f"Response Status Code: {response.status_code}")
        print(f"Response Body: {response.text}")
        print(f"Request Duration: {duration:.2f} seconds")

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
    make_post_request(api_url, payload)

if __name__ == "__main__":
    main()
