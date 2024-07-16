# main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
import pandas as pd

app = FastAPI()

# Mount the 'static' directory to serve Streamlit app
app.mount("/streamlit", StaticFiles(directory="streamlit"), name="streamlit")

@app.get("/")
def read_root():
    return {"message": "Hello World!"}

@app.get("/data")
def get_data():
    df = pd.read_csv('data/formation7.csv')
    return df.to_dict(orient='records')

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
