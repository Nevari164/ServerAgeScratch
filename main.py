import scratchattach as scratch
import time
from fastapi import FastAPI

app = FastAPI()

# Initialize Scratch cloud connection
session = scratch.login("Prettingminecraft", "5arkansas6")
project = session.connect_cloud(1097165205)  # Replace with your project ID

# Global control variable
should_update = True

# Endpoint to stop the updater
@app.post("/stop")
async def stop_updating():
    global should_update
    should_update = False
    return {"status": "Cloud variable updater stopped"}

# Endpoint to start the updater
@app.post("/start")
async def start_updating():
    global should_update
    if should_update:
        return {"status": "Updater already running"}
    should_update = True
    return {"status": "Cloud variable updater started"}

# Main cloud updater function
def update_cloud_variable():
    global should_update
    start_time = time.time()
    while should_update:
        elapsed_time = int(time.time() - start_time)
        project.set_var("runtime", elapsed_time)
        time.sleep(1)

# Run updater in background
import threading
threading.Thread(target=update_cloud_variable, daemon=True).start()
