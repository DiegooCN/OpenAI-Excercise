# List of functions that the AI can use
def say_hello():

    """Saluda al usuario cada vez que empieza una conversación o cuando el usuario lo solicite"""

    prompt = f"""¡Hola! Bienvenid@ al chat de Movistar!\nEstoy para ayudare en:\n• Conocer detalle de tu deuda\n• Formas y lugares de pago\n• Solicitar Recibo\nComentanos, ¿Qué necesitas?"""

    return prompt

def ask_dni():

    """Pregunta el DNI del usuario"""

    prompt = """\nPor favor ingresa tu DNI, Recuerda que el DNI debe tener 9 dígitos"""
    return prompt

def validate_dni(dni):
    
    """Valida el DNI del usuario"""

    prompt = "DNI Inválido, ingrese nuevamente"
    available_dni = ["123456789", "987654321"]

    if len(dni) == 9:
        if dni in available_dni:
            prompt = say_hello()

    return prompt














def out_of_context():

    """Responde cuando el usuario pregunta algo que no está dentro de las funciones que el bot puede realizar"""

    prompt = """\nEl tema que me preguntas no está dentro de mi contexto,\npor favor pregunta algo que esté relacionado con las funciones que\nte mostré al anteriormente"""

    return prompt

def get_method_payment_locations():

    """Muestra las formas y lugares de pago"""

    prompt = """\nFORMAS Y LUGARES DE PAGO\nEn Movistar te brindamos diversas formas de pago SIN COMISIÓN.\nPuedes pagar por Yape https://innovacxion.page.link/mVFa\ndesde la web o app de tu banco.\nConoce todos los canales de pago en el siguiente link\nhttps://www.movistar.com.pe/atencion-al-cliente/lugares-y-medios-de-pago"""
    return prompt   

def get_receipt():

    """Muestra el link para solicitar el recibo"""

    prompt = """\nSOLICITAR RECIBO\nObten tu recibo con solo unos clics\nhttps://mirecibo.movistar.com.pe"""
    return prompt

def get_debt_detail(dni):

    """Muestra el detalle de la deuda"""

    available_dni = ["123456789", "987654321"]

    if dni in available_dni:
        prompt = f"""\nDETALLE DE DEUDA\nTu deuda al día de hoy es de S/ 10.00\nTu fecha de vencimiento es el 12/07/2023\nTu DNI: {dni}"""
    else:
        prompt = f"""\nTu DNI: {dni} no se encuentra registrado en nuestra base de datos\nPor favor ingresa un DNI válido"""
    return prompt

def say_goodbye():

    """Se despide del usuario cuando este lo solicite"""

    prompt = """\nGracias por usar el servicio de asistencia de Movistar\n¡Hasta pronto!"""

    return prompt