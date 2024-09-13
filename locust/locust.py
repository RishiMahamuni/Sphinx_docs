import json
from locust import HttpUser, TaskSet, task, between

# Load configuration dynamically from config.json
with open("config.json") as config_file:
    config = json.load(config_file)

class UserBehavior(TaskSet):
    @task
    def test_long_running_api(self):
        with self.client.post(config["endpoint"], json=config["payload"], catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Failed with status code {response.status_code}")

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(config["min_wait"] / 1000, config["max_wait"] / 1000)  # Converting milliseconds to seconds
