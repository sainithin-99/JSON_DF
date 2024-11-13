from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Dict, Any
import pandas as pd
import queue
import threading
import time

app = FastAPI()

class Item(BaseModel):
    data: List[Dict[str, Any]]

# Create a queue to store the incoming requests
request_queue = queue.Queue()

# Function to process the queue
def process_queue():
    while True:
        item = request_queue.get()
        if item is None:
            break
        try:
            # Convert JSON data to Pandas DataFrame
            df = pd.DataFrame(item.data)
            # You can now use the DataFrame `df` as needed
            print(df)
        except Exception as e:
            print(f"An error occurred while processing the data: {e}")
        finally:
            request_queue.task_done()

# Start a background thread to process the queue
thread = threading.Thread(target=process_queue, daemon=True)
thread.start()

@app.post("/convert-to-df/")
async def convert_to_df(item: Item, background_tasks: BackgroundTasks):
    try:
        # Add the request to the queue
        request_queue.put(item)
        # Add a background task to ensure the request is processed
        background_tasks.add_task(process_queue)
        return {"message": "Data received and will be processed in FCFS order."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"An error occurred: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
