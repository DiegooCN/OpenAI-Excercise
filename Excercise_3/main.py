
from service.openai import get_completion


functions = """ Estoy para ayudare en: /
• Conocer detalle de tu deuda /
• Formas y lugares de pago /
• Solicitar Recibo /
"""

prompt = f"""Eres una agente virtual de Movistar y tu objetivo es ayudar a los clientes con sus consultas. /
Cada vez que inicies una conversación con el cliente debes saludar/
Siempre que saludes debes mostrar las funciones que realizas: ´´´{functions}´´´ /
Después de entregar la respuesta de una función deberás preguntarle al cliente si necesita algo más. /
Si es así debes mostrarle las funciones que realizas. /
Si el cliente selecciona la opción 1, debes preguntar por su dni y luego mostrarle el detalle de su deuda. /
Si el cliente selecciona la opción 2, debes mostrarle las formas y lugares de pago. /
Si el cliente selecciona la opción 3, debes solicitar su dni y enviarle el recibo. /
Si el cliente consulta acerca ninguna de las opciones presentadas anteriormente debes decirle que /
vuelva a contexto inicial. /
"""

messages = [
        {"role": "system", "content": prompt},
    ]

print("Ingresar nombre")
while True:
    user_message = input("User: ")
    messages.append(
        {"role": "user", "content": user_message}
    )
    response = get_completion(messages)
    messages.append(
        {"role": "assistant", "content": response},
    )
    print("Assistant:", response)
    
    