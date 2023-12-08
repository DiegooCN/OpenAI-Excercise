from openai_handler import get_completions


behavior = """Eres un asistente de Movistar, debes ayudar a los usuarios a resolver dudas. \
    debes ser capaz de identificar el contexto de la conversación y responder de acuerdo a ello. \
    Debes llamar a la función say_hello() para iniciar la conversación."""

messages = [
    {"role": "system", "content": behavior},
]


while True:
    messages.append({"role": "assistant", "content":  get_completions(messages)})
    print("Assistant: ", get_completions(messages))
    user_input = input("User: ")
    messages.append({"role": "user", "content": user_input})

    
