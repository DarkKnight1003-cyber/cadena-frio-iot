from flask import Flask, request, jsonify
import mysql.connector
import csv
import os
from datetime import datetime
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

app = Flask(__name__)


def conectar():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )


@app.route("/")
def inicio():
    return "Servidor de cadena de frio funcionando"


@app.route("/datos", methods=["POST"])
def recibir_datos():
    datos = request.get_json()
    temperatura = datos["temperatura"]
    humedad = datos["humedad"]

    # alerta si la temperatura sale del rango de 2 a 8 grados
    alerta = temperatura < 2 or temperatura > 8
    fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # guardar en la base de datos
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute(
        "INSERT INTO lecturas (temperatura, humedad, alerta) VALUES (%s, %s, %s)",
        (temperatura, humedad, alerta)
    )
    conexion.commit()
    cursor.close()
    conexion.close()

    # guardar en el csv
    archivo_nuevo = not os.path.exists("lecturas.csv")
    with open("lecturas.csv", "a", newline="") as archivo:
        escritor = csv.writer(archivo)
        if archivo_nuevo:
            escritor.writerow(["fecha_hora", "temperatura", "humedad", "alerta"])
        escritor.writerow([fecha_hora, temperatura, humedad, alerta])

    return jsonify({"mensaje": "dato guardado", "alerta": alerta})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)