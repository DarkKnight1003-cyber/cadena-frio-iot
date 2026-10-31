
import time
from getpass import getpass
from threading import Event
import paho.mqtt.client as mqtt

# Datos de prueba: temperatura y humedad
lecturas = [
    (5.0, 60.0),
    (6.5, 62.0),
    (9.5, 65.0),
    (1.5, 58.0),
    (5.5, 61.0)
]

conectado = Event()

def al_conectar(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("Conectado a Mosquitto AWS")
    else:
        print("Conexion rechazada:", reason_code)
    conectado.set()

client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2,
    client_id="simulador-cadena-frio"
)

client.username_pw_set(
    "cadena_frio_iot",
    getpass("Contrasena MQTT: ")
)

client.on_connect = al_conectar
client.connect("127.0.0.1", 1883, 60)
client.loop_start()

if not conectado.wait(10) or not client.is_connected():
    client.loop_stop()
    raise SystemExit("No se pudo establecer la conexion MQTT")

print("Iniciando simulacion de cadena de frio...")

try:
    while True:
        for temperatura, humedad in lecturas:
            estado = (
                "ALERTA" if temperatura < 2 or temperatura > 8
                else "NORMAL"
            )

            datos = {
                "temperatura": temperatura,
                "humedad": humedad,
                "alerta": estado
            }

            for nombre, valor in datos.items():
                mensaje = client.publish(
                    f"invernadero1/{nombre}",
                    str(valor),
                    qos=1,
                    retain=True
                )
                mensaje.wait_for_publish()

            print(
                f"Temp: {temperatura} C | "
                f"Humedad: {humedad}% | {estado}"
            )

            time.sleep(5)

except KeyboardInterrupt:
    print("Simulacion detenida")

finally:
    client.disconnect()
    client.loop_stop()

import time
from getpass import getpass
from threading import Event
import paho.mqtt.client as mqtt

# Datos de prueba: temperatura y humedad
lecturas = [
    (5.0, 60.0),
    (6.5, 62.0),
    (9.5, 65.0),
    (1.5, 58.0),
    (5.5, 61.0)
]

conectado = Event()

def al_conectar(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("Conectado a Mosquitto AWS")
    else:
        print("Conexion rechazada:", reason_code)
    conectado.set()

client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2,
    client_id="simulador-cadena-frio"
)

client.username_pw_set(
    "cadena_frio_iot",
    getpass("Contrasena MQTT: ")
)

client.on_connect = al_conectar
client.connect("127.0.0.1", 1883, 60)
client.loop_start()

if not conectado.wait(10) or not client.is_connected():
    client.loop_stop()
    raise SystemExit("No se pudo establecer la conexion MQTT")

print("Iniciando simulacion de cadena de frio...")

try:
    while True:
        for temperatura, humedad in lecturas:
            estado = (
                "ALERTA" if temperatura < 2 or temperatura > 8
                else "NORMAL"
            )

            datos = {
                "temperatura": temperatura,
                "humedad": humedad,
                "alerta": estado
            }

            for nombre, valor in datos.items():
                mensaje = client.publish(
                    f"invernadero1/{nombre}",
                    str(valor),
                    qos=1,
                    retain=True
                )
                mensaje.wait_for_publish()

            print(
                f"Temp: {temperatura} C | "
                f"Humedad: {humedad}% | {estado}"
            )

            time.sleep(5)

except KeyboardInterrupt:
    print("Simulacion detenida")

finally:
    client.disconnect()
    client.loop_stop()
