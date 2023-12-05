import json
import openai
import os

from dotenv import load_dotenv

from service.payment import get_method_payment_locations, get_debt_detail

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def get_completion(messages):

    tools = [
        {
            "type": "function",
            "function": {   
                "name": "get_method_payment_locations",
                "description": "Obtiene los métodos de pago disponibles, junto a ubicaciones para pagar.",
                "parameters": {
                    "type": "object",
                    "properties": {}
                },
            }
        },
        {
            "type": "function",
            "function": {   
                "name": "get_debt_detail",
                "description": "Obtiene el detalle de la deuda del cliente.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "message": {
                            "type": "string",
                            "description": "Mensaje del cliente",
                        }
                    }
                },
            }
        },
    ]


    response = openai.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=messages,
        temperature=0.8, # this is the degree of randomness of the model's output
        tools=tools,
        tool_choice="auto"
    )

    functions = response.choices[0].message.tool_calls

    if functions:
        avaliable_functions = {
            "get_method_payment_locations": get_method_payment_locations,
            "get_debt_detail": get_debt_detail,
        }

        for function in functions:
            function_name = function.function.name
            function_to_call = avaliable_functions[function_name]
            function_args = json.loads(function.function.arguments)
            function_response = function_to_call(
                message=function_args.get("message")
            )
            messages.append({
                "role": "system",
                "content": function_response,
            })

        final_response = openai.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=messages
        )
        
        return final_response.choices[0].message.content
    
        

    else:
        return response.choices[0].message.content