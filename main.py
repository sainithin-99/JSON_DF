from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import pandas as pd

app = FastAPI()

class Item(BaseModel):
    data: List[Dict[str, Any]]

@app.post("/convert-to-df/")
async def convert_to_df(item: Item):
    try:
        # Convert JSON data to Pandas DataFrame
        df = pd.DataFrame(item.data)
        # You can now use the DataFrame `df` as needed
        print(df)
        return {"message": "Data received and converted to DataFrame successfully."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"An error occurred: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


-------------------------------------------------------------------------------
curl -X 'POST' \
  'http://127.0.0.1:8000/convert-to-df/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "data": [
    {"name": "John", "age": 30, "city": "New York"},
    {"name": "Anna", "age": 22, "city": "London"},
    {"name": "Mike", "age": 32, "city": "Chicago"}
  ]
}'
