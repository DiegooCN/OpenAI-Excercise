import os
import json

from functions import say_hello , out_of_context , get_method_payment_locations , get_receipt, say_goodbye, get_debt_detail, ask_dni, to_many_tries, validate_dni
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

behavior = """Tu objetivo es clasificar analizar lo que dice el usuario y responder con la función que más se adecue a ella. \
    Las funciones que puedes utilizar son: \
        > Saludar \
        > Preguntar por DNI \
        > Métodos y lugares de pago \
        > Obtener recibo \
        > Despedirse \
        > Obtener detalle deuda \
        > Fuera de contexto \
    Solo puedes devolver el nombre de las funciones."""

messages = [
    {"role": "system", "content": behavior},
    {"role": "system", "content": "say_hello"},
]

tools=[
    {
        "type": "function",
        "function": {
            "name": "function_handler",
            "description": "Retorna un mensaje especifico",
            "parameters": {
                "type": "object",
                "properties": {
                    "messages": {
                        "type": "array",
                    }
                },
            },
        },
    }
]

def get_completion(messages):

    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=messages,
        tools=tools,
        tool_choice={
            "function": "function_handler",
        }
    )

    message_response = response.choices[0].message.content

    messages.append({"role": "assistant", "content": message_response})

    return message_response

while True:
    print("**********************************")
    print(get_completion(messages))
    user_input = input("User: ")
    messages.append({"role": "user", "content": user_input})


    
