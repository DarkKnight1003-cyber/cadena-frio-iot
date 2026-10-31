# Grafana

Instalado en la EC2 pública; disponible por defecto en `127.0.0.1:3000` y accesible desde Windows a través de un túnel SSH. La fuente de datos **InfluxDB** está configurada con lenguaje de consulta **Flux**, organización `cadena_frio`, bucket `lecturas_iot` y URL privada `http://10.0.13.49:8086`. El token no se publica.

Dashboard `Monitoreo de Cadena de Frío IoT`:

1. Serie temporal de temperatura (`temperatura`, grados Celsius).
2. Serie temporal de humedad (`humedad`, porcentaje).
3. Indicador Stat del campo `alerta` (0 → NORMAL en verde, 1 → ALERTA en rojo).

Regla `Alerta de temperatura fuera de rango`: consulta los últimos 60 segundos, usa el máximo del campo binario `alerta`, condición `Max > 0`, evaluación por minuto, sin período de espera y sin retención al normalizarse. Contacto de correo electrónico mediante SMTP configurado **solo en el servidor**; no compartir la contraseña de aplicación. Se verificó la recepción de un correo automático `[FIRING:1]`.

**Exportación adicional recomendada:** en el dashboard, usar *Share/Export* o *Dashboard settings → JSON model* (según la versión) para guardar un JSON **sin credenciales** como `dashboard.json`.
