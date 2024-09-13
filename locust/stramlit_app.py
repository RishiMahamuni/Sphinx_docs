import os
import streamlit as st
import json

# UI form to get load testing parameters
st.title("Locust Load Testing UI")

host = st.text_input("Host URL", value="http://localhost:8000")
endpoint = st.text_input("API Endpoint", value="/api/test")
users = st.number_input("Number of Users", value=100, min_value=1)
spawn_rate = st.number_input("Spawn Rate", value=10, min_value=1)
run_time = st.text_input("Run Time (e.g., 5m, 10m)", value="5m")
min_wait = st.number_input("Minimum Wait Time (seconds)", value=1)
max_wait = st.number_input("Maximum Wait Time (seconds)", value=5)
payload = st.text_area("Request Payload (JSON)", value='{"key1": "value1", "key2": "value2"}')

# Save the inputs to config.json dynamically
if st.button("Start Load Test"):
    # Write the config file
    config = {
        "endpoint": endpoint,
        "min_wait": min_wait,
        "max_wait": max_wait,
        "payload": json.loads(payload)
    }
    
    with open("config.json", "w") as config_file:
        json.dump(config, config_file)
    
    # Run Locust with the provided inputs
    os.system(f"locust -f locustfile.py --host={host} --users={users} --spawn-rate={spawn_rate} --run-time={run_time}")
    st.success("Load test started!")
