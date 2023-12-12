import os
import json

from controller import function_handler
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

behavior = """Tu objetivo es clasificar analizar lo que dice el usuario y responder con el nombre de la función que más se adecue a ella. \
    Las funciones que puedes utilizar son: \
        > say_hello \
        > method_payment \
        > payment_places \
        > say_goodbye \
        > get_debt_detail \
        > out_of_context \
    Ejemplo:\
        > User: Hola\
        > Assistant: say_hello\
        > User: Quiero pagar mi deuda\
        > Assistant: get_debt_detail"""

messages = [
    {"role": "system", "content": behavior},
    {"role": "assistant", "content": "say_hello"},
]

def get_completion(messages):

    tools=[
        {
            "type": "function",
            "function": {
                "name": "function_handler",
                "description": "Returns a message based on the user input.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "function": {
                            "type": "string",
                            "description": "The function to be executed.",
                        },
                    },
                    "required": ["function"],
                },
            },
        }
    ]

    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=messages,
        tools=tools,
        tool_choice={
            "type": "function",
            "function": {
                "name": "function_handler"
            }
        }
    )


    tool_args = json.loads(response.choices[0].message.tool_calls[0].function.arguments)
    print("Action: " ,tool_args.get("function")) 

    function_response = function_handler(messages=messages, function=tool_args.get("function"))

    messages.append({"role": "assistant", "content": function_response})

    return function_response

while True:
    print("**********************************")
    print(get_completion(messages))
    user_input = input("User: ")
    messages.append({"role": "user", "content": user_input})


    
