# Cadena de frío IoT

Este proyecto es la práctica 1 de Inteligencia Artificial aplicada a Internet de las Cosas. Simula una caja de transporte de vacunas y medicamentos: una ESP32 con un sensor DHT22 mide la temperatura y la humedad, las envía por WiFi a un servidor hecho en Flask, y el servidor las guarda en un archivo CSV y en una base de datos MySQL. Si la temperatura sale del rango de 2 °C a 8 °C, la lectura se marca como alerta. La humedad solo se registra, porque no tiene un límite estándar.

## Cómo ponerlo a funcionar

1. Instala Python desde python.org, marcando la casilla "Add python.exe to PATH" antes de darle a Install.
2. Instala MySQL Server y MySQL Workbench con el instalador de MySQL (instalación personalizada) y crea la contraseña del usuario root.
3. Descarga este proyecto con el botón verde "Code" y luego "Download ZIP", y descomprímelo.
4. Abre la carpeta en una terminal y crea el entorno virtual con `python -m venv venv`.
5. Actívalo con `.\venv\Scripts\Activate.ps1`.
6. Instala las librerías con `pip install -r requirements.txt`.
7. En Workbench entra a la instancia local, abre el archivo `crear_tabla.sql` con File > Open SQL Script y ejecútalo con el rayo amarillo.
8. Copia `config.example.py`, ponle el nombre `config.py` y cambia la contraseña por la tuya.
9. Corre el servidor con `python app.py`.
10. En otra terminal, manda una lectura de prueba con `Invoke-RestMethod -Uri http://127.0.0.1:5000/datos -Method Post -ContentType "application/json" -Body '{"temperatura": 5.2, "humedad": 48}'` y revisa que aparezca en `lecturas.csv` y en Workbench con `SELECT * FROM cadena_frio.lecturas;`.