import scratchattach as scratch
import time


# Initialize Scratch cloud connection
session = scratch.login("Prettingminecraft", "5arkansas6")
project = session.connect_cloud(1097165205)  # Replace with your project ID
offset = 60000
# Global control variable
should_update = True
start_time = time.time()
while True:
 timer = int(time.time() - start_time) + offset
 project.set_var("runtime2",timer)
 time.sleep(1)
