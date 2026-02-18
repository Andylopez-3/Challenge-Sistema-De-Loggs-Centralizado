🛡️ Centralized Logging Service (API REST)

Este proyecto consiste en un Servicio de Logging Centralizado diseñado bajo una arquitectura Cliente-Servidor. Permite que múltiples microservicios envíen sus logs de eventos a un servidor centralizado que los almacena y permite su consulta mediante filtros avanzados.

This project is a Centralized Logging Service designed under a Client-Server architecture. It allows multiple microservices to send event logs to a centralized server that stores them and enables querying through advanced filters.

🏗️ Architecture / Arquitectura

El sistema se divide en dos componentes principales:
The system is divided into two main components:

Server (Flask + SQLite): Recibe los logs, valida la identidad del servicio mediante un Token de Autorización, normaliza los datos y los persiste.
Receives logs, validates service identity via Authorization Token, normalizes data, and persists it.

Client (Requests): Simula un servicio activo que genera ráfagas de logs aleatorios y los envía de forma eficiente en un solo paquete JSON.
Simulates an active service that generates bursts of random logs and sends them efficiently in a single JSON package.

🚀 Key Features / Características Principales

Token Authentication: Seguridad robusta mediante encabezados Authorization. ¡Respuesta personalizada ante accesos no autorizados! ("Mávapa nde?").

Batch Processing: El servidor soporta el envío de un solo log o una lista de logs (batch), optimizando el tráfico de red y reduciendo la cantidad de peticiones HTTP.

Advanced Querying: Endpoint GET con soporte para filtros de fecha y hora (timestamp y received_at) usando parámetros de consulta (Query Params).

Security Testing: El sistema fue probado con tokens erróneos para garantizar que solo los servicios autorizados puedan persistir datos.

🛠️ Tech Stack / Tecnologías Usadas

Backend: Python 3.x, Flask.

Database: SQLite3.

Testing: Requests library (Client simulation).

🔍 API Endpoints / Puntos de Acceso

POST /logs
Envía uno o más logs al servidor. / Send one or multiple logs.

Header: Authorization: Token <YOUR_TOKEN>

Body (JSON):

JSON
{
  "timestamp": "2024-05-20 10:00:00",
  "service": "MemeService",
  "severity": "ERROR",
  "message": "Error 404: Dignidad no encontrada"
}

GET /logs
Consulta logs con filtros opcionales. / Query logs with optional filters.

Parámetros disponibles: timestamp_start, timestamp_end, received_at_start, received_at_end.

📊 Database Schema / Esquema de DatosLa tabla logs cuenta con la siguiente estructura para auditoría:The logs table has the following structure for auditing purposes:

Campo        Tipo        Descripción  
id           INTEGER     Clave primaria autoincremental.
timestamp    TEXT        Fecha/hora original del evento (generada por el cliente)
received_at  TEXT        Fecha/hora de recepción (generada por el servidor).
service      TEXT        Nombre del servicio emisor (Auth, Payment, Meme, etc.).
severity     TEXT        Nivel de importancia (INFO, WARNING, CRITICAL, etc.).
message      TEXT        Descripción detallada del evento.

🔧 Installation & Usage / Instalación y Uso

Instalar dependencias:
Bash
pip install flask requests

Iniciar el servidor:
Bash
python servidor.py

Ejecutar el cliente (simulador):
Bash
python cliente.py
