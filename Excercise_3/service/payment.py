


def get_method_payment_locations():
    prompt = """Debes mostrar el siguiente mensaje:
    <FORMAS Y LUGARES DE PAGO \
    En Movistar te brindamos diversas formas de pago SIN COMISIÓN. \
    Puedes pagar por Yape \
    https://innovacxion.page.link/mVFa \
    desde la web o app de tu banco. \
    Conoce todos los canales de pago en el siguiente link \
    https://www.movistar.com.pe/atencion-al-cliente/lugares-y-medios-de-pago> \  
    Si el cliente desea ver otra función debes permitirle mostrar las funciones ya descritas anteriormente. \
    """
    return prompt

def get_debt_detail(message):
    prompt = f"""Debes preguntar por el DNI del cliente y luego mostrarle el detalle de su deuda. \
    El formato del DNI debe ser de 8 dígitos. \
    si no te muestra un DNI correcto, pedirle que ingrese nuevamente su DNI, si falla dos veces mostrar las funciones \
    a las que puede acceder. \
    
    El formato del detalle de la deuda debe ser el siguiente: \
    <DETALLE DE DEUDA \
    'nombre del cliente' Tienes un recibo pendiente de tu servicio HOGAR \
    12312 que venció el 12/12 por S/10.000 \
    ¿Contamos con tu pago para hoy o mañana? \ 


    Mensaje del cliente: {message} \
    """
    return prompt

def get_receipt():
    print("Recipt")
    return True