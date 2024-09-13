import json
import os

# Load the config from config.json
with open("config.json") as config_file:
    config = json.load(config_file)

# Construct the command to run Locust using the config values
command = f"locust -f locustfile.py --host={config['host']} --users={config['users']} --spawn-rate={config['spawn_rate']} --run-time={config['run_time']}"

# Run the command
os.system(command)
