import os
import json

from dotenv import load_dotenv
from openai import OpenAI
from functions import function_handler

load_dotenv()

openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

tools = [
    {
        "type": "function",
        "function": {
            "name": "function_handler",
            "description": "Selecciona una función para responder al usuario",
            "parameters": {
                "type": "object",
                "properties": {
                    "messages": {
                        "type": "string",
                        "Description": "El contexto de la conversación",
                    }
                },
                "required": ["messages"],
            },
        },
    },
]

def get_completions(messages):
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=messages,
        tools=tools,
        tool_choice= {
            "type": "function",
            "function": {
                "name": "function_handler"
            }
        },
        temperature=0.5,
    )

    tool_calls = response.choices[0].message.tool_calls

    avaliable_tools = {
        "function_handler": function_handler,
    }

    for tool in tool_calls:
        tool_name= tool.function.name
        tool_to_call = avaliable_tools[tool_name]
        tool_args = json.loads(tool.function.arguments)
        tool_response = tool_to_call(
            messages=tool_args.get("messages")
        )
    return tool_response