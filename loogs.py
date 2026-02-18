from flask import Flask, request, jsonify  #importamos flask para crear la api , request para manejar las solicitudes y jsonify para devolver respuestas en formato JSON
import sqlite3                     #importamos sqlite3 para manejar la base de datos SQLite
from datetime import datetime   #importamos datetime para manejar fechas y horas

app = Flask(__name__)   #creamos una instancia de la aplicacion Flask
NOMBRE_BD = "logs.db"         #nombre de la base de datos SQLite


TOKENS_SERVICIO = {         #diccionario que contiene los tokens de autenticacion para cada servicio
    "AuthService": "TOKEN_AUTH_123",
    "PaymentService": "TOKEN_PAY_456",
    "MemeService": "TOKEN_MEME_789"
}


def inicializar_bd():   #funcion para inicializar la base de datos y crear la tabla logs si no existe
    conexion = sqlite3.connect(NOMBRE_BD)
    cursor_bd = conexion.cursor()
    cursor_bd.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT, /* timestamp del log enviado por el servicio */
            received_at TEXT, /* timestamp cuando el servidor recibe el log */
            service TEXT,          /* nombre del servicio que envio el log */
            severity TEXT,          /* severidad del log */
            message TEXT               /* mensaje del log */
        )
    """)
    conexion.commit()    #guardamos los cambios en la base de datos
    conexion.close()      #cerramos la conexion a la base de datos

def es_token_valido(cabecera_autorizacion):
    if not cabecera_autorizacion or not cabecera_autorizacion.startswith("Token "):  # es para saber si lo que viene no tiene cabecera o no empieza con "token"  
        return False               # si no tiene cabecera o no empieza con "token" devuelve falso , es para saber si el tojen es valido o no
    token = cabecera_autorizacion.split(" ")[1]     # separamos el token del prefijo "Token "
    return token in TOKENS_SERVICIO.values()               # verificamos si el token esta en los valores de los tokens permitidos


@app.route("/logs", methods=["POST"])  #ruta para recibir logs via POST
def recibir_log():
    cabecera = request.headers.get("Authorization")        # obtenemos la cabecera de autorizacion de la solicitud
    if not es_token_valido(cabecera):     # verificamos si el token es valido
        return jsonify({"error": "Mávapa nde?"}), 401  # si el token no es valido devolvemos un error 401 que significa que no esta autorizado para enviar logs        

    datos = request.get_json()         # obtenemos los datos JSON enviados en la solicitud
    
    # 2. Normalizar a lista (para soportar uno o muchos logs)
    lista_logs = datos if isinstance(datos, list) else [datos] # si los datos ya son una lista los dejamos asi , 
                                                        #pero si no lo convertimos igual , para poder procesarlos todos de la misma forma    
    
    conexion = sqlite3.connect(NOMBRE_BD)    # conectamos a la base de datos
    cursor_bd = conexion.cursor()   
    ahora_server = datetime.now().strftime("%Y-%m-%d %H:%M:%S") # obtenemos la fecha y hora actual del servidor en formato string

    try:
        for log in lista_logs:  # iteramos sobre cada log en la lista de logs
            
            # Validar campos mínimos
            if not all(k in log for k in ("timestamp", "service", "severity", "message")): # verificamos que cada logs tenga los datos que requiere el servidor
                continue # Salta logs mal formados
            
            cursor_bd.execute("""
                INSERT INTO logs (timestamp, received_at, service, severity, message)
                VALUES (?, ?, ?, ?, ?)      /* usamos placeholders para evitar inyeccion SQL*/
            """, (log["timestamp"], ahora_server, log["service"], log["severity"], log["message"])) # insertamos el log en la base de datos
        
        conexion.commit()
        return jsonify({"status": "Logs guardados exitosamente", "cantidad": len(lista_logs)}), 201 # si paso todo bien devolvemos un mensaje que diga que se guardaron los logs
    except Exception as e:                                                                         # y devolvemos con 201 para avisar que se creo correctamente , y que se guardo en bd
        return jsonify({"error": str(e)}), 500   # si hubo un error devolvemos un mensaje de error con codigo 500 , que es que hubo un error interno del servidor
    finally:
        conexion.close()       # y pase lo que pase cerramos la conexion a la base de datos , ya sea que haya habido un error o no
    

@app.route("/logs", methods=["GET"])        #ruta para obtener logs via GET con filtros opcionales
def obtener_logs():     # funcion para obtener logs con filtros opcionales
    condiciones = [] # lista para almacenar las condiciones del WHERE
    params = []    # lista para almacenar los parametros de las condiciones

  
    filtros = {           # diccionario con los posibles filtros
        "timestamp >= ?": request.args.get("timestamp_start"),   # con el resquest.args.get obtenemos los parametros que vienen en la URL con el metodo GET
        "timestamp <= ?": request.args.get("timestamp_end"),       #y .get toma el valor del parametro que  le puso el cliente puso como filtro 
        "received_at >= ?": request.args.get("received_at_start"),
        "received_at <= ?": request.args.get("received_at_end")
    }

    for query, valor in filtros.items():  # iteramos sobre los filtros
        if valor:         # si el valor del filtro no es None
            condiciones.append(query)        # agregamos la condicion al WHERE
            params.append(valor)          # agregamos el valor del filtro a los parametros

    sql = "SELECT * FROM logs"   # consultamos todos los logs que haya en la base de datos 
    if condiciones:            # si hay condiciones para el WHERE 
        sql += " WHERE " + " AND ".join(condiciones)    # agregamos las condiciones , para las consultas  sql , los unimos con AND , para que todas se cumplan a la vez
    sql += " ORDER BY received_at DESC" # Ordenados por lo más reciente

    conexion = sqlite3.connect(NOMBRE_BD)
    cursor_bd = conexion.cursor() 
    cursor_bd.execute(sql, params)    # le pasamos los valores de los parametros para evitar inyeccion SQL
    filas = cursor_bd.fetchall()        # obtenemos todas las filas resultantes
    conexion.close()

    resultado = [
        {"id": f[0],                # id del log
        "timestamp": f[1],      # timestamp del log enviado por el servicio
        "received_at": f[2],    # timestamp cuando el servidor recibe el log
        "service": f[3],          # nombre del servicio que envio el log
        "severity": f[4],           # severidad del log
        "message": f[5]}                # mensaje del log
        for f in filas              # iteramos sobre cada fila y creamos un diccionario con los datos del log
    ]

    return jsonify(resultado), 200          # devolvemos el resultado en formato JSON con codigo 200 , que significa que todo salio bien

if __name__ == "__main__":
    inicializar_bd()           # inicializamos la base de datos al iniciar el servidor
    print(" Servidor de Logging corriendo en http://localhost:5000")
    app.run(debug=True)      # iniciamos la aplicacion Flask en modo debug  , que es para desarrollo y pruebas  , por que te permite ver errores detallados y
                            #recargar automaticamente el servidor al hacer cambios en el codigo sin tener que reiniciarlo manualmente

