import fastapi
import os

from dotenv import load_dotenv
from openai import OpenAI
from database import getMessages, saveMessage
from models import User, Context
from service import get_date

# Load the environment variables
load_dotenv()
env = {
    "OPENAI_API_KEY" : os.environ.get('OPENAI_API_KEY')
}

app = fastapi.FastAPI()

openai = OpenAI(api_key=env["OPENAI_API_KEY"])

@app.post("/send-response")
def send_message(user: User):

    context = Context(user=user)

    behavior = 'Eres una agente virtual llamada MIA, tu función es responder las preguntas de los usuarios'
    
    chat_history = [
            {"role": "system" , "content" : behavior},
    ]

    messages_to_add = getMessages(user)

    for message in messages_to_add:
        chat_history.append({
            "role": message["role"],
            "content": message["content"],
        })
    messages= {"role": "user" , "content" : user.message}
        
    chat_history.append(messages)

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
        messages=chat_history,
        tools=tools,
        tool_choice="auto"
    )

    response_messages = response.choices[0].message
    tool_calls = response.choices[0].message.tool_calls

    context.content = user.message
    context.role = "user"
    saveMessage(context)

    if tool_calls:

        available_tools = {
            "get_date" : get_date()
        }

        for tool_call in tool_calls:
            tool_name = tool_call.function.name
            tool_to_call = available_tools[tool_name]
            tool_response = tool_to_call
            chat_history.append({
                    "role": "system",
                    "content": tool_response,
            })

        final_response = openai.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=chat_history
        )
        
        context.content = final_response.choices[0].message.content
        context.role = final_response.choices[0].message.role
        saveMessage(context)

        return final_response

    else:

        context.content = response_messages.content
        context.role = response_messages.role
        saveMessage(context)
        
        return response 

