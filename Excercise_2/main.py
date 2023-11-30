import uuid
import fastapi
import os

from dotenv import load_dotenv
from openai import OpenAI
from database import isUser
from models import User
from service import get_date

load_dotenv()

app = fastapi.FastAPI()

openai = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

@app.post("/send-response")
def send_message(user: User):

    user.id = user.id if isUser(user) else str(uuid.uuid4())

    behavior = f'Eres una agente virtual llamada MIA y tu objetivo es decir la fecha a {user.name}'

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
    
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )

    response_messages = response.choices[0].message
    tool_calls = response.choices[0].message.tool_calls

    if tool_calls:

        available_tools = {
            "get_date" : get_date()
        }

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

