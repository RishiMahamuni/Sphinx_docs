import json
from locust import HttpUser, TaskSet, task, between

# Load configuration dynamically from config.json
with open("config.json") as config_file:
    config = json.load(config_file)

class UserBehavior(TaskSet):
    @task
    def get_request(self):
        self.client.get(config["endpoint"])

    @task
    def post_request(self):
        self.client.post(config["endpoint"], json=config["payload"])

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(config["min_wait"], config["max_wait"])
