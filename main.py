from fastapi import FastAPI, BackgroundTasks
import scratchattach as scratch
import time

app = FastAPI()

# Global runtime tracker and connection
start_time = None
connection = None

def update_cloud_variable(username, password, project_id):
    global start_time, connection

    # Log in and connect to Scratch
    session = scratch.login(username, password)
    connection = session.connect_cloud(project_id)

    print("Connected to Scratch cloud variables.")

    # Start tracking runtime
    start_time = time.time()

    try:
        while True:
            if connection is None:
                break
            # Calculate runtime in seconds
            runtime_seconds = int(time.time() - start_time)

            # Update cloud variable
            connection.set_var("runtime", runtime_seconds)

            print(f"Updated runtime to {runtime_seconds} seconds.")
            time.sleep(1)  # Update every second
    except Exception as e:
        print("Error updating cloud variable:", e)

@app.get("/")
async def root():
    return {"message": "Scratch Cloud Variable Updater"}

@app.post("/start")
async def start_updater(
    username: str, password: str, project_id: str, background_tasks: BackgroundTasks
):
    """
    Start updating the cloud variable in the background.
    """
    global start_time, connection
    if connection is not None:
        return {"error": "Updater is already running."}

    background_tasks.add_task(update_cloud_variable, username, password, project_id)
    return {"status": "Started updating cloud variable."}

@app.post("/stop")
async def stop_updater():
    """
    Stop the cloud variable updater.
    """
    global connection
    if connection is None:
        return {"error": "No updater is running."}

    connection = None
    return {"status": "Stopped updating cloud variable."}
