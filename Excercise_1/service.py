import requests
import fastapi
import json
import os
from dotenv import load_dotenv 

load_dotenv()

app = fastapi.FastAPI()

@app.get("/get-date")
def get_date():
    url = os.environ.get('DATE_API_URL')
    response = requests.get(url)
    date = response.json()
    return {"date": date['fecha_actual']}

