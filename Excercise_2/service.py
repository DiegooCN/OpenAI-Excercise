import requests
import fastapi
import os
import json

from dotenv import load_dotenv

load_dotenv()

env = {
    "DATE_API_URL" : os.environ.get('DATE_API_URL')
}

app = fastapi.FastAPI()

@app.get("/get-date")
def get_date():
    url = env["DATE_API_URL"]
    response = requests.get(url)
    if response.status_code == 200:
        return json.dumps(response.json())