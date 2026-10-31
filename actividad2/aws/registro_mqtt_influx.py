
import csv
from pathlib import Path
from datetime import datetime, timezone
from getpass import getpass

import paho.mqtt.client as mqtt
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

# ===== CONFIGURACION =====
MQTT_HOST = "127.0.0.1"
MQTT_PORT = 1883
MQTT_USER = "cadena_frio_iot"

INFLUX_URL = "http://10.0.13.49:8086"
INFLUX_ORG = "cadena_frio"
INFLUX_BUCKET = "lecturas_iot"

# Cambiar a "esp32" cuando usemos el sensor real
ORIGEN = "simulador"

CSV_PATH = Path.home() / "cadena-frio-datos" / "lecturas.csv"
CSV_PATH.parent.mkdir(parents=True, exist_ok=True)

# ===== CREDENCIALES =====
mqtt_password = getpass("Contrasena MQTT: ")
influx_token = getpass("Token InfluxDB: ")

# ===== CONEXION INFLUXDB =====
influx = InfluxDBClient(
    url=INFLUX_URL,
    token=influx_token,
    org=INFLUX_ORG,
    timeout=10000
)

write_api = influx.write_api(write_options=SYNCHRONOUS)

# ===== ARCHIVO CSV =====
if not CSV_PATH.exists():
    with open(CSV_PATH, "w", newline="") as archivo:
        csv.writer(archivo).writerow([
            "fecha_utc", "temperatura", "humedad", "estado"
        ])

lectura = {}

# ===== MQTT =====
def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("MQTT conectado")
        client.subscribe("invernadero1/+")
    else:
        print("Error MQTT:", reason_code)


def on_message(client, userdata, msg):
    if msg.retain:
        return

    campo = msg.topic.split("/")[-1]

    if campo not in ("temperatura", "humedad", "alerta"):
        return

    lectura[campo] = msg.payload.decode()

    if campo != "alerta":
        return

    if not all(k in lectura for k in (
        "temperatura", "humedad", "alerta"
    )):
        print("Lectura incompleta")
        lectura.clear()
        return

    try:
        temperatura = float(lectura["temperatura"])
        humedad = float(lectura["humedad"])
        estado = lectura["alerta"]
        fecha = datetime.now(timezone.utc)

        # ===== GUARDAR CSV =====
        with open(CSV_PATH, "a", newline="") as archivo:
            csv.writer(archivo).writerow([
                fecha.isoformat(timespec="seconds"),
                temperatura,
                humedad,
                estado
            ])

        # ===== GUARDAR INFLUXDB =====
        punto = (
            Point("cadena_frio")
            .tag("origen", ORIGEN)
            .field("temperatura", temperatura)
            .field("humedad", humedad)
            .field("alerta", 1 if estado == "ALERTA" else 0)
            .field("estado", estado)
            .time(fecha)
        )

        write_api.write(
            bucket=INFLUX_BUCKET,
            org=INFLUX_ORG,
            record=punto
        )

        print(
            f"CSV OK | InfluxDB OK | "
            f"Temp: {temperatura} C | "
            f"Humedad: {humedad}% | {estado}",
            flush=True
        )

    except Exception as error:
        print("Error guardando datos:", error, flush=True)

    finally:
        lectura.clear()


cliente = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2,
    client_id="registro-influx-cadena-frio"
)

cliente.username_pw_set(MQTT_USER, mqtt_password)
cliente.on_connect = on_connect
cliente.on_message = on_message

print("Iniciando almacenamiento MQTT -> CSV + InfluxDB")

try:
    cliente.connect(MQTT_HOST, MQTT_PORT, 60)
    cliente.loop_forever()
except KeyboardInterrupt:
    print("Registro detenido")
finally:
    cliente.disconnect()
    influx.close()

import csv
from pathlib import Path
from datetime import datetime, timezone
from getpass import getpass

import paho.mqtt.client as mqtt
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

# ===== CONFIGURACION =====
MQTT_HOST = "127.0.0.1"
MQTT_PORT = 1883
MQTT_USER = "cadena_frio_iot"

INFLUX_URL = "http://10.0.13.49:8086"
INFLUX_ORG = "cadena_frio"
INFLUX_BUCKET = "lecturas_iot"

# Cambiar a "esp32" cuando usemos el sensor real
ORIGEN = "simulador"

CSV_PATH = Path.home() / "cadena-frio-datos" / "lecturas.csv"
CSV_PATH.parent.mkdir(parents=True, exist_ok=True)

# ===== CREDENCIALES =====
mqtt_password = getpass("Contrasena MQTT: ")
influx_token = getpass("Token InfluxDB: ")

# ===== CONEXION INFLUXDB =====
influx = InfluxDBClient(
    url=INFLUX_URL,
    token=influx_token,
    org=INFLUX_ORG,
    timeout=10000
)

write_api = influx.write_api(write_options=SYNCHRONOUS)

# ===== ARCHIVO CSV =====
if not CSV_PATH.exists():
    with open(CSV_PATH, "w", newline="") as archivo:
        csv.writer(archivo).writerow([
            "fecha_utc", "temperatura", "humedad", "estado"
        ])

lectura = {}

# ===== MQTT =====
def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("MQTT conectado")
        client.subscribe("invernadero1/+")
    else:
        print("Error MQTT:", reason_code)


def on_message(client, userdata, msg):
    if msg.retain:
        return

    campo = msg.topic.split("/")[-1]

    if campo not in ("temperatura", "humedad", "alerta"):
        return

    lectura[campo] = msg.payload.decode()

    if campo != "alerta":
        return

    if not all(k in lectura for k in (
        "temperatura", "humedad", "alerta"
    )):
        print("Lectura incompleta")
        lectura.clear()
        return

    try:
        temperatura = float(lectura["temperatura"])
        humedad = float(lectura["humedad"])
        estado = lectura["alerta"]
        fecha = datetime.now(timezone.utc)

        # ===== GUARDAR CSV =====
        with open(CSV_PATH, "a", newline="") as archivo:
            csv.writer(archivo).writerow([
                fecha.isoformat(timespec="seconds"),
                temperatura,
                humedad,
                estado
            ])

        # ===== GUARDAR INFLUXDB =====
        punto = (
            Point("cadena_frio")
            .tag("origen", ORIGEN)
            .field("temperatura", temperatura)
            .field("humedad", humedad)
            .field("alerta", 1 if estado == "ALERTA" else 0)
            .field("estado", estado)
            .time(fecha)
        )

        write_api.write(
            bucket=INFLUX_BUCKET,
            org=INFLUX_ORG,
            record=punto
        )

        print(
            f"CSV OK | InfluxDB OK | "
            f"Temp: {temperatura} C | "
            f"Humedad: {humedad}% | {estado}",
            flush=True
        )

    except Exception as error:
        print("Error guardando datos:", error, flush=True)

    finally:
        lectura.clear()


cliente = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2,
    client_id="registro-influx-cadena-frio"
)

cliente.username_pw_set(MQTT_USER, mqtt_password)
cliente.on_connect = on_connect
cliente.on_message = on_message

print("Iniciando almacenamiento MQTT -> CSV + InfluxDB")

try:
    cliente.connect(MQTT_HOST, MQTT_PORT, 60)
    cliente.loop_forever()
except KeyboardInterrupt:
    print("Registro detenido")
finally:
    cliente.disconnect()
    influx.close()
