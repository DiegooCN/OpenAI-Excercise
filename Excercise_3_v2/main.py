import os
import json

from functions import say_hello , out_of_context , get_method_payment_locations , get_receipt, say_goodbye, get_debt_detail, ask_dni, to_many_tries, validate_dni
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

behavior = """Eres un asistente de Movistar y debes seguir las siguientes fases en orden: \
    > Fase 1: \
        - Saludar al usuario al comienzo de la conversación. \
        - Solicitar su DNI para continuar con las consultas. \
        - Validar el DNI ingresado por el usuario. \
    > Fase 2: \
        - Una vez el DNI sea válido, no volver a preguntar. \
        - Responder lo que pide el usuario teniendo en cuenta el contexto de la conversación. \
        - Utilizar solo las funciones que se indican. \
    > Fase 3: \
        - Despedirse del usuario cuando este lo solicite.\
    REGLAS: \
        - No puedes mostrar el recibo, deuda o formas/lugares de pago sin antes haber validado el DNI del usuario.\
        - Si el usuario ingresa un mensaje sin sentido, decirle que esta fuera de contexto.\
        - Si el usuario se equivoca 3 veces al ingresar el DNI llamar a la función 'to_many_tries'"""

messages = [
    {"role": "system", "content": behavior},
]

functions = {
        "say_hello": say_hello(),
        "out_of_context": out_of_context(),
        "get_method_payment_locations": get_method_payment_locations(),
        "get_receipt": get_receipt(),
        "say_goodbye": say_goodbye(),
        "ask_dni": ask_dni(),
        "to_many_tries":to_many_tries()
    }

functions_with_args = {
        "get_debt_detail": get_debt_detail,
        "validate_dni": validate_dni,
}

def get_completion(messages):

    tools = [
        {
            "type": "function",
            "function": {
                "name": "say_hello",
                "description": "Saludar al usuario cada vez que empieza una conversación o cuando el usuario salude",
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
                "name": "ask_dni",
                "description": "Pregunta el DNI del usuario",
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
                "name": "validate_dni",
                "description": "Valida el DNI del usuario",
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
                "name": "to_many_tries",
                "description": "El usuario ingresa más de dos veces un DNI incorrecto",
                "parameters": {
                    "type": "object",
                    "properties": {},
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
            if tool_name in functions_with_args :
                tool_to_call = functions_with_args[tool_name] 
                tool_args = json.loads(tool.function.arguments)
                tool_response = tool_to_call(tool_args.get("dni"))
                messages.append({"role": "assistant","content": tool_response})
            else:
                tool_to_call = functions[tool_name] 
                tool_response = tool_to_call
                messages.append({"role": "assistant","content": tool_response})
        return tool_response
    return out_of_context()

while True:
    print("**********************************")
    print(get_completion(messages))
    user_input = input("User: ")
    messages.append({"role": "user", "content": user_input})


    
