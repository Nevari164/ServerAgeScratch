from flask import Flask
import time
from threading import Thread
import scratchconnect
# Initialize Flask app
app = Flask(__name__)

# Initialize Scratch cloud connection


user = scratchconnect.ScratchConnect("Prettingminecraft", "5arkansas6")
project = user.connect_project(project_id=1097165205)
variables = project.connect_cloud_variables()
#variables.get_variable_data(limit=100, offset=0)  # Returns the cloud variable data
#variables.get_cloud_variable_value(variable_name="Name", limit=100)  # Returns the cloud variable value
# Program to set cloud variables:

#session = scratch.login("Prettingminecraft", "5arkansas6")
#project = session.connect_cloud(1097165205)  # Replace with your project ID
offset = 60000
should_update = True
start_time = time.time()

# Background task to update the Scratch variable
def update_timer():
    global start_time
    while should_update:
        timer = int(time.time() - start_time) + offset
        set = variables.set_cloud_variable(variable_name="runtime2", value=timer)  # Set a Cloud Variable
        if set:
         print("Cloud Variable Updated!")
       # project.set_var("runtime2", timer)
        time.sleep(1)

# Start the background thread for the timer update
timer_thread = Thread(target=update_timer)
timer_thread.daemon = True  # This allows the thread to exit when the main program ends
timer_thread.start()

@app.route('/')
def home():
    return "Scratch timer is running..."

@app.route('/stop')
def stop():
    global should_update
    should_update = False  # Stop the background task
    return "Timer stopped."

if __name__ == '__main__':
    app.run(debug=True)
