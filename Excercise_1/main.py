from openai import OpenAI
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel

import os

# Load the environment variables
load_dotenv()

# Create an instance of the OpenAI class
openai = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Create an instance of the FastAPI class
app = FastAPI()

class User(BaseModel):
    name: str
    message: str

@app.post("/get-response")
def get_response(user: User):

    # Create a prompt
    behavior = f'Eres una agente virtual llamada MIA y tu objetivo es decir la fecha a {user.name}'

    # Create a completion
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=[
            {"role": "system" , "content" : behavior},
            {"role": "user" , "content" : user.message}
        ],
        tools=[
            {
                "type": "function",
                "function": {   
                    "name": "get_date",
                    "description": "Get the date from the API",
                    "parameters": {
                        "type": "object",
                        "properties": {}
                    },
                }
            }
        ],
        tool_choice="auto"
    )

    return response