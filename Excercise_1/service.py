import requests
import os

def get_date():
    response = requests.get(os.environ.get('DATE_API_URL'))
    return response.json()