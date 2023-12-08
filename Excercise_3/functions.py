import os
import json

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Create a function that returns a response based on the logic reasoning from the AI
def function_handler(messages):

    functions = {
        "say_hello": say_hello(),
        "out_of_context": out_of_context(),
        "show_options": show_options(),
        "get_method_payment_locations": get_method_payment_locations(),
        "get_receipt": get_receipt(),
    }

    behavior = f"""
        Debes elegir una de las siguientes funciones <{functions}> que se adecuen mejor a lo que el usuario pide, debes analizar el mensaje <{messages}> y \
        debes responder por qué elegiste esa opción \
        Retorna en un json con las siguientes keys: \
        thoughts = Tu razonamiento \
        response = El return de la función elegida \
        """
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=[{"role": "system", "content": behavior}],
    )

    final_response = json.loads(response.choices[0].message.content)

    # print("Thoughts: ", final_response["thoughts"])

    return final_response["response"]

# List of functions that the AI can use
def say_hello():

    """Saluda al usuario cada vez que empieza una conversación o cuando el usuario lo solicite"""

    options = show_options()
    prompt = f"""Hola, soy un bot de Movistar\n{options}"""

    return prompt, options 

def out_of_context():

    """Responde cuando el usuario pregunta algo que no está dentro de las funciones que el bot puede realizar"""

    prompt = """\nEl tema que me preguntas no está dentro de mi contexto,\n \
        por favor pregunta algo que esté relacionado con las funciones que\n \
        te mostré al anteriormente"
        """

    return prompt

def show_options():

    """Muestra las funciones que el bot puede realizar"""

    prompt = """Estoy para ayudare en:\n• Conocer detalle de tu deuda\n• Formas y lugares de pago\n• Solicitar Recibo\n"""

    return prompt

def get_method_payment_locations():

    """Muestra las formas y lugares de pago"""

    prompt = """FORMAS Y LUGARES DE PAGO\nEn Movistar te brindamos diversas formas de pago SIN COMISIÓN.\nPuedes pagar por Yape https://innovacxion.page.link/mVFa\ndesde la web o app de tu banco. Conoce todos los canales de pago en el siguiente link\nhttps://www.movistar.com.pe/atencion-al-cliente/lugares-y-medios-de-pago"""
    return prompt   

def get_receipt():

    """Muestra el link para solicitar el recibo"""

    prompt = """SOLICITAR RECIBO \
            Obten tu recibo con solo unos clics \
            https://mirecibo.movistar.com.pe \
                """
    return prompt
