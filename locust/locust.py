import json
from locust import HttpUser, TaskSet, task, between

# Load configuration from config.json
with open("config.json") as config_file:
    config = json.load(config_file)

# Load payload from payload.json
with open("payload.json") as payload_file:
    payload = json.load(payload_file)

class UserBehavior(TaskSet):
    @task
    def post_request(self):
        # Make the POST request with the payload loaded from the file
        with self.client.post(config["endpoint"], json=payload, catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Failed with status code {response.status_code}")

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(config["min_wait"] / 1000, config["max_wait"] / 1000)