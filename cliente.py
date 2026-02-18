import requests  # exportamos la libreria requests para hacer peticiones HTTP
import time         # exportamos la libreria time para manejar tiempos y demoras
from datetime import datetime # exportamos datetime para manejar fechas y horas
import random   # exportamos random para generar datos aleatorios

URL = "http://localhost:5000/logs" # URL del servidor de logs
TOKEN = "TOKEN_PAY_456"    # token de autenticacion para el servicio

def generar_log(nombre_servicio):      # funcion para generar logs de prueba
    niveles = ["INFO", "DEBUG", "WARNING", "ERROR", "CRITICAL"]       # niveles de severidad posibles
    mensajes = [                    # mensajes de log de ejemplo
        "Sistema iniciado correctamente",
        "Falla en la conexión de base de datos",
        "Usuario intentó subir un meme prohibido",
        "Latencia alta en el proceso de pago",
        "Error 404: Dignidad no encontrada"
    ]
    
    return {                               # generamos un log con datos aleatorios
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "service": nombre_servicio,
        "severity": random.choice(niveles),
        "message": random.choice(mensajes)
    }

def enviar_rafaga(cantidad=10):     # funcion para enviar una ráfaga de logs al servidor
    headers = {"Authorization": f"Token {TOKEN}"}      # cabeceras de la solicitud con el token de autenticacion
    
    # 1. Creamos una LISTA vacía para guardar los logs
    lista_de_logs = []
    
    print(f" Preparando {cantidad} logs...")
    for _ in range(cantidad):
        # Generamos un log nuevo en cada vuelta y lo metemos en la lista
        nuevo_log = generar_log("MemeService")
        lista_de_logs.append(nuevo_log)
        time.sleep(0.5)  # Simular tiempo entre logs
    
    # 2. Ahora sí, enviamos LA LISTA COMPLETA en un solo viaje
    print(f" Enviando paquete de {len(lista_de_logs)} logs al servidor...")
    
    try:
        r = requests.post(URL, json=lista_de_logs, headers=headers)  # enviamos la solicitud POST al servidor con los logs
        print(f"Status: {r.status_code} - Respuesta: {r.json()}")       # mostramos el estado de la respuesta y el contenido
    except Exception as e:
        print(f" Error de conexión: {e}")       # manejamos errores de conexion

if __name__ == "__main__":
    # Enviamos una ráfaga de prueba
    enviar_rafaga(10)
