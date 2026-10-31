# ESP32 MQTT — Actividad 2

Colocar en esta carpeta el sketch **`esp32_mqtt.ino`** que se compiló y probó con el ESP32 y sensor DHT22. El sketch requiere su configuración privada **`secrets.h`**, que se mantiene solamente en el equipo local y **no se sube a GitHub**.

Dependencias en Arduino IDE: placa *ESP32 by Espressif Systems*, bibliotecas *PubSubClient*, *DHT sensor library* (Adafruit) y las dependencias necesarias.

Tópicos empleados:

- `invernadero1/temperatura`
- `invernadero1/humedad`
- `invernadero1/alerta`

La autenticación MQTT está habilitada. Las mediciones se publican aproximadamente cada cinco segundos.

Para usar un nuevo broker, ajustar el host y las credenciales en el `secrets.h` local según las constantes que usa el sketch.
