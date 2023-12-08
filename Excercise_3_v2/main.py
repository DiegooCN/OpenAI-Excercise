import os
import json

from functions import say_hello , out_of_context , show_options , get_method_payment_locations , get_receipt, say_goodbye, get_debt_detail, ask_dni
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

behavior = """Eres un asistente de Movistar y debes hacer lo siguiente:\
    - Identificar el contexto de la conversación.\
    - Saludar al usuario cada vez que empieza una conversación o cuando el usuario lo solicite.\
    - Solicitar su DNI para continuar con las consultas.
    - Responder siempre utilizando una {function} que se adecue al contexto de la conversación.
    - Despedirse del usuario cuando este lo solicite.
    """

messages = [
    {"role": "system", "content": behavior},
]

functions = {
        "say_hello": say_hello(),
        "out_of_context": out_of_context(),
        "show_options": show_options(),
        "get_method_payment_locations": get_method_payment_locations(),
        "get_receipt": get_receipt(),
        "say_goodbye": say_goodbye(),
        "get_debt_detail": get_debt_detail,
        "ask_dni": ask_dni(),
    }



def get_completion(messages):

    tools = [
        {
            "type": "function",
            "function": {
                "name": "say_hello",
                "description": "Saluda al usuario cada vez que empieza una conversación o cuando el usuario lo salude",
                "parameters": {
                    "type": "object",
                    "properties": {}
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "out_of_context",
                "description": "Cuando el usuario pregunta algo que no está dentro de las funciones que el bot puede realizar responde con este mensaje",
                "parameters": {
                    "type": "object",
                    "properties": {}
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "show_options",
                "description": "Muestra las funciones disponibles las cuales el bot puede realizar",
                "parameters": {
                    "type": "object",
                    "properties": {}
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "get_method_payment_locations",
                "description": "Muestra las formas y lugares de pago",
                "parameters": {
                    "type": "object",
                    "properties": {}
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "get_receipt",
                "description": "Muestra el link para solicitar el recibo",
                "parameters": {
                    "type": "object",
                    "properties": {}
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "say_goodbye",
                "description": "Se despide del usuario cuando este lo solicite",
                "parameters": {
                    "type": "object",
                    "properties": {}
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "get_debt_detail",
                "description": "Muestra el detalle de la deuda",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "dni": {
                            "type": "string",
                        },
                    },
                    "required": ["dni"],
                },
                
            },
        },
        {
            "type": "function",
            "function": {
                "name": "ask_dni",
                "description": "Pregunta el DNI del usuario",
                "parameters": {
                    "type": "object",
                    "properties": {}
                },
            },
        },
    ]

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )

    tool_calls = response.choices[0].message.tool_calls

    if tool_calls:

        for tool in tool_calls:
            tool_name = tool.function.name
            print("Tool name: ", tool_name)
            tool_to_call = functions[tool_name] 
            if tool_name == "get_debt_detail":
                tool_args = json.loads(tool.function.arguments)
                tool_response = tool_to_call(tool_args.get("dni"))
                messages.append({"role": "assistant","content": tool_response})
            else:
                tool_response = tool_to_call
                messages.append({"role": "assistant","content": tool_response})
        return tool_response
    
    else:
        return say_hello()

while True:
    print("**********************************")
    print(get_completion(messages))
    user_input = input("User: ")
    messages.append({"role": "user", "content": user_input})


    
