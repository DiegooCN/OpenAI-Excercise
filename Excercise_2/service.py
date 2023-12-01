import requests
import fastapi
import json
import os
from dotenv import load_dotenv 

load_dotenv()

env = {
    "DATE_API_URL" : os.environ.get('DATE_API_URL')
}

app = fastapi.FastAPI()

@app.get("/get-date")
def get_date():
    url = env.DATE_API_URL
    response = requests.get(url)
    date = response.json()
    return json.dumps(date)

