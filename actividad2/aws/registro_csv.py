
import csv
from datetime import datetime, timezone
from pathlib import Path
from getpass import getpass
import paho.mqtt.client as mqtt

# ===== CONFIGURACION =====
BROKER = "127.0.0.1"
PUERTO = 1883
USUARIO = "cadena_frio_iot"

# Archivo donde guardaremos las mediciones
ARCHIVO = Path.home() / "cadena-frio-datos" / "lecturas.csv"
ARCHIVO.parent.mkdir(parents=True, exist_ok=True)

# Crear encabezados si el archivo no existe
if not ARCHIVO.exists():
    with open(ARCHIVO, "w", newline="") as f:
        csv.writer(f).writerow([
            "fecha_utc",
            "temperatura",
            "humedad",
            "estado"
        ])

# Almacenar temporalmente los valores recibidos
lectura = {}

def al_conectar(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("Conectado a Mosquitto")
        client.subscribe("invernadero1/+")
    else:
        print("Error de conexion:", reason_code)

def al_mensaje(client, userdata, msg):
    # Ignorar valores antiguos retenidos por Mosquitto
    if msg.retain:
        return

    campo = msg.topic.split("/")[-1]
    if campo not in ("temperatura", "humedad", "alerta"):
        return

    lectura[campo] = msg.payload.decode()

    # Registrar cuando llega el ultimo dato de la lectura
    if campo == "alerta" and all(
        k in lectura for k in ("temperatura", "humedad", "alerta")
    ):
        try:
            temperatura = float(lectura["temperatura"])
            humedad = float(lectura["humedad"])
            estado = lectura["alerta"]

            fecha = datetime.now(timezone.utc).isoformat(
                timespec="seconds"
            )

            with open(ARCHIVO, "a", newline="") as f:
                csv.writer(f).writerow([
                    fecha, temperatura, humedad, estado
                ])

            print(
                f"{fecha} | Temp: {temperatura} C | "
                f"Humedad: {humedad}% | {estado}"
            )

        except ValueError:
            print("Lectura invalida, no se guarda")

        lectura.clear()

# ===== CLIENTE MQTT =====
cliente = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2,
    client_id="registro-csv-aws"
)

cliente.username_pw_set(
    USUARIO,
    getpass("Contrasena MQTT: ")
)

cliente.on_connect = al_conectar
cliente.on_message = al_mensaje

print("Iniciando registro automatico en CSV...")
print("Archivo:", ARCHIVO)

cliente.connect(BROKER, PUERTO, 60)
cliente.loop_forever()

import csv
from datetime import datetime, timezone
from pathlib import Path
from getpass import getpass
import paho.mqtt.client as mqtt

# ===== CONFIGURACION =====
BROKER = "127.0.0.1"
PUERTO = 1883
USUARIO = "cadena_frio_iot"

# Archivo donde guardaremos las mediciones
ARCHIVO = Path.home() / "cadena-frio-datos" / "lecturas.csv"
ARCHIVO.parent.mkdir(parents=True, exist_ok=True)

# Crear encabezados si el archivo no existe
if not ARCHIVO.exists():
    with open(ARCHIVO, "w", newline="") as f:
        csv.writer(f).writerow([
            "fecha_utc",
            "temperatura",
            "humedad",
            "estado"
        ])

# Almacenar temporalmente los valores recibidos
lectura = {}

def al_conectar(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("Conectado a Mosquitto")
        client.subscribe("invernadero1/+")
    else:
        print("Error de conexion:", reason_code)

def al_mensaje(client, userdata, msg):
    # Ignorar valores antiguos retenidos por Mosquitto
    if msg.retain:
        return

    campo = msg.topic.split("/")[-1]
    if campo not in ("temperatura", "humedad", "alerta"):
        return

    lectura[campo] = msg.payload.decode()

    # Registrar cuando llega el ultimo dato de la lectura
    if campo == "alerta" and all(
        k in lectura for k in ("temperatura", "humedad", "alerta")
    ):
        try:
            temperatura = float(lectura["temperatura"])
            humedad = float(lectura["humedad"])
            estado = lectura["alerta"]

            fecha = datetime.now(timezone.utc).isoformat(
                timespec="seconds"
            )

            with open(ARCHIVO, "a", newline="") as f:
                csv.writer(f).writerow([
                    fecha, temperatura, humedad, estado
                ])

            print(
                f"{fecha} | Temp: {temperatura} C | "
                f"Humedad: {humedad}% | {estado}"
            )

        except ValueError:
            print("Lectura invalida, no se guarda")

        lectura.clear()

# ===== CLIENTE MQTT =====
cliente = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2,
    client_id="registro-csv-aws"
)

cliente.username_pw_set(
    USUARIO,
    getpass("Contrasena MQTT: ")
)

cliente.on_connect = al_conectar
cliente.on_message = al_mensaje

print("Iniciando registro automatico en CSV...")
print("Archivo:", ARCHIVO)

cliente.connect(BROKER, PUERTO, 60)
cliente.loop_forever()
