import re
from datetime import datetime

def validar_nombre(nombre):
    return re.fullmatch(r"[A-Za-zÁÉÍÓÚáéíóúñÑ ]+", nombre) is not None

def validar_puesto(puesto):
    return re.fullmatch(r"[A-Za-zÁÉÍÓÚáéíóúñÑ ]+", puesto) is not None

def validar_id(id):
    return id.isdigit()

def validar_codigo(codigo):
    return codigo.isdigit()

def validar_telefono(telefono):
    return telefono.isdigit() and len(telefono) == 10

def validar_correo(correo):
    return re.fullmatch(r"[^@ \t\r\n]+@[^@ \t\r\n]+\.[a-zA-Z]+", correo) is not None

def validar_fecha(fecha):
    # Primero verifica que coincida con el formato básico
    if not re.fullmatch(r"\d{2}/\d{2}/\d{4}", fecha):
        return False
    try:
        # Luego intenta convertirla en una fecha real
        datetime.strptime(fecha, "%d/%m/%Y")
        return True
    except ValueError:
        return False
    
def validar_direccion(direccion):
    return bool(direccion.strip())  # Verifica que no esté vacío
    
def validar_especialidad(especialidad):
    return re.fullmatch(r"[A-Za-zÁÉÍÓÚáéíóúñÑ ]+", especialidad) is not None   

def validar_contacto(contacto):
    return bool(contacto.strip())  # Verifica que no esté vacío 

def validar_precio(precio):
    return re.fullmatch(r"^\d+(\.\d{1,2})?$", precio) is not None  # Verifica que sea un número con hasta dos decimales

def validar_costo(costo):
    return re.fullmatch(r"^\d+(\.\d{1,2})?$", costo) is not None  # Verifica que sea un número con hasta dos decimales

def validar_existencias(existencias):
    return existencias.isdigit() and int(existencias) >= 0  # Verifica que sea un número entero no negativo

def validar_importe(importe):
    return re.fullmatch(r"^\d+(\.\d{1,2})?$", importe) is not None

def validar_motivo(motivo):
    return bool(motivo.strip())

def validar_cantidad(cantidad):
    return cantidad.isdigit() and int(cantidad) > 0

def validar_subtotal(subtotal):
    return re.fullmatch(r"^\d+(\.\d{1,2})?$", subtotal) is not None

def mostrar_mensaje_error(tipo):
    mensajes = {
        "nombre": "El campo Nombre solo debe contener letras.",
        "telefono": "El campo Teléfono debe ser de 10 dígitos y no puede contener letras.",
        "correo": "El campo Correo debe tener el formato micorreo@correo.com.",
        "id": "El campo ID solo debe contener números.",
        "puesto": "El campo Puesto solo debe contener letras.",
        "fecha": "El campo Fecha debe ser una fecha válida y tener el formato dd/mm/aaaa.",
        "especialidad": "El campo Especialidad solo debe contener letras.",
        "direccion": "El campo Dirección debe estar lleno",
        "contacto": "El campo Contacto no puede estar vacío.",
        "codigo": "El campo Código solo debe contener números.",
        "precio": "El campo Precio debe ser un número con hasta dos decimales.",
        "costo": "El campo Costo debe ser un número con hasta dos decimales.",
        "existencias": "El campo Existencias debe ser un número entero.",
        "importe": "El campo Importe debe ser un número con hasta dos decimales.",
        "motivo": "El campo Motivo debe estar lleno.",
        "cantidad": "El campo Cantidad deber estar lleno.",
        "subtotal": "El campo Subtotal debe ser un número con hasta dos decimales."
    }
    return mensajes.get(tipo, "Dato inválido.")