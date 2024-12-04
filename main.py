from flask import Flask, request
import time
from threading import Thread
import scratchconnect

# Initialize Flask app
app = Flask(__name__)

# Initialize Scratch cloud connection
user = scratchconnect.ScratchConnect("Prettingminecraft", "5arkansas6")
project = user.connect_project(project_id=1097165205)
variables = project.connect_cloud_variables()

# Global variables for managing the timer and update state
offset = 60000
should_update = False  # Initially, the timer is not running
start_time = None

# Background task to update the Scratch cloud variable
def update_timer():
    global start_time
    while should_update:
        timer = int(time.time() - start_time) + offset
        set = variables.set_cloud_variable(variable_name="runtime2", value=timer)  # Set a Cloud Variable
        if set:
            print("Cloud Variable Updated!")
        time.sleep(1)

# Start the background thread for the timer update
def start_timer():
    global start_time, should_update
    should_update = True
    start_time = time.time()  # Start the timer
    # Start the background thread to update the cloud variable
    timer_thread = Thread(target=update_timer)
    timer_thread.daemon = True  # This allows the thread to exit when the main program ends
    timer_thread.start()

@app.route('/start', methods=['POST'])
def start():
    # Start the timer when a POST request is received
    if not should_update:
        start_timer()
        return "Timer started!"
    else:
        return "Timer is already running."

@app.route('/stop', methods=['POST'])
def stop():
    global should_update
    should_update = False  # Stop the background task
    return "Timer stopped."

@app.route('/')
def home():
    return "Scratch timer is running..."

if __name__ == '__main__':
    app.run(debug=True)
