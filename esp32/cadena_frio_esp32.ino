#include <WiFi.h>
#include <HTTPClient.h>
#include "DHT.h"

// ---- Datos que cada quien debe cambiar ----
const char* ssid = "NOMBRE_DE_TU_WIFI";
const char* password = "CLAVE_DE_TU_WIFI";
const char* servidor = "http://IP_DE_TU_COMPUTADOR:5000/datos";

// true con el sensor conectado, false para probar con datos falsos
const bool USAR_SENSOR = true;

// ---- Sensor ----
#define DHTPIN 4
#define DHTTYPE DHT22
DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(115200);
  dht.begin();

  WiFi.begin(ssid, password);
  Serial.print("Conectando al WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println();
  Serial.print("Conectado. IP de la ESP32: ");
  Serial.println(WiFi.localIP());
}

void loop() {
  float temperatura;
  float humedad;

  if (USAR_SENSOR) {
    temperatura = dht.readTemperature();
    humedad = dht.readHumidity();
    if (isnan(temperatura) || isnan(humedad)) {
      Serial.println("Error leyendo el DHT22");
      delay(2000);
      return;
    }
  } else {
    // datos falsos para probar sin sensor
    temperatura = random(20, 110) / 10.0;
    humedad = random(400, 700) / 10.0;
  }

  Serial.print("Temperatura: ");
  Serial.print(temperatura);
  Serial.print(" C  Humedad: ");
  Serial.println(humedad);

  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(servidor);
    http.addHeader("Content-Type", "application/json");

    String json = "{\"temperatura\": " + String(temperatura) +
                  ", \"humedad\": " + String(humedad) + "}";

    int codigo = http.POST(json);
    Serial.print("Respuesta del servidor: ");
    Serial.println(codigo);
    http.end();
  } else {
    Serial.println("WiFi desconectado");
  }

  delay(5000);
}