from openai import OpenAI
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from service import get_date

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

@app.post("/send-response")
def send_message(user: User):

    # Create a prompt
    behavior = f'Eres una agente virtual llamada MIA y tu objetivo es decir la fecha a {user.name}'

    # Setting the messages and tools
    messages=[
            {"role": "system" , "content" : behavior},
            {"role": "user" , "content" : user.message}
        ]
    
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
        ]
    
    # Create a completion
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )

    response_messages = response.choices[0].message
    tool_calls = response.choices[0].message.tool_calls

    if tool_calls:

        available_tools = {"get_date" : get_date()}

        for tool_call in tool_calls:
            tool_name = tool_call.function.name
            tool_to_call = available_tools[tool_name]
            tool_response = tool_to_call
            messages.append({
                    "role": "system",
                    "content": tool_response,
            })

        final_response = openai.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=messages
        )
        
        return final_response

    else:
        return response_messages    
        
            