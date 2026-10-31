
#include <WiFi.h>
#include <PubSubClient.h>
#include "DHT.h"
#include "secrets.h"

// ===== SENSOR DHT22 =====
#define DHTPIN 4
#define DHTTYPE DHT22

DHT dht(DHTPIN, DHTTYPE);

// true = sensor real; false = datos simulados
const bool USAR_SENSOR = true;

// ===== MQTT =====
WiFiClient wifiClient;
PubSubClient mqtt(wifiClient);

const char* TOPIC_TEMP = "invernadero1/temperatura";
const char* TOPIC_HUM = "invernadero1/humedad";
const char* TOPIC_ALERTA = "invernadero1/alerta";

// ===== TIEMPOS =====
const unsigned long INTERVALO = 5000;

unsigned long ultimaLectura = 0;
unsigned long ultimoIntentoWiFi = 0;
unsigned long ultimoIntentoMQTT = 0;

void setup() {
  Serial.begin(115200);
  dht.begin();

  // Conectar al WiFi
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

  Serial.println("Iniciando cadena de frio...");

  // Configurar servidor MQTT de AWS
  mqtt.setServer(MQTT_SERVER, MQTT_PORT);
}

void loop() {

  // ===== VERIFICAR WIFI =====
  if (WiFi.status() != WL_CONNECTED) {
    if (millis() - ultimoIntentoWiFi >= INTERVALO) {
      ultimoIntentoWiFi = millis();
      Serial.println("Reconectando WiFi...");
      WiFi.reconnect();
    }
    return;
  }

  // ===== VERIFICAR MQTT =====
  if (!mqtt.connected()) {
    if (ultimoIntentoMQTT == 0 ||
        millis() - ultimoIntentoMQTT >= INTERVALO) {

      ultimoIntentoMQTT = millis();

      String clientId = "esp32-cadena-frio-" + WiFi.macAddress();
      clientId.replace(":", "");

      Serial.println("Conectando a Mosquitto AWS...");

      if (mqtt.connect(clientId.c_str(),
                       MQTT_USER, MQTT_PASSWORD)) {
        Serial.println("MQTT conectado correctamente");
      } else {
        Serial.print("Error MQTT, estado: ");
        Serial.println(mqtt.state());
      }
    }
    return;
  }

  mqtt.loop();

  // ===== LEER DATOS CADA 5 SEGUNDOS =====
  if (millis() - ultimaLectura < INTERVALO) {
    return;
  }

  ultimaLectura = millis();

  float temperatura;
  float humedad;

  if (USAR_SENSOR) {
    temperatura = dht.readTemperature();
    humedad = dht.readHumidity();

    if (isnan(temperatura) || isnan(humedad)) {
      Serial.println("Error leyendo el DHT22");
      return;
    }
  } else {
    temperatura = random(20, 110) / 10.0;
    humedad = random(400, 700) / 10.0;
  }

  // ===== DETECTAR ALERTA =====
  bool alerta = temperatura < 2.0 || temperatura > 8.0;

  String tempTexto = String(temperatura, 1);
  String humTexto = String(humedad, 1);

  // ===== PUBLICAR EN MQTT =====
  bool enviadoTemp = mqtt.publish(TOPIC_TEMP,
                                  tempTexto.c_str(), true);

  bool enviadoHum = mqtt.publish(TOPIC_HUM,
                                 humTexto.c_str(), true);

  bool enviadoAlerta = mqtt.publish(
    TOPIC_ALERTA,
    alerta ? "ALERTA" : "NORMAL",
    true
  );

  // ===== MOSTRAR RESULTADOS =====
  Serial.print("Temperatura: ");
  Serial.print(temperatura);
  Serial.print(" C | Humedad: ");
  Serial.print(humedad);
  Serial.print(" % | Estado: ");
  Serial.println(alerta ? "ALERTA" : "NORMAL");

  if (enviadoTemp && enviadoHum && enviadoAlerta) {
    Serial.println("Datos publicados en MQTT");
  } else {
    Serial.println("Error al publicar datos");
  }
}
