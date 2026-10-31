# Consultas Flux utilizadas en Grafana

## Temperatura

```flux
from(bucket: "lecturas_iot")
  |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
  |> filter(fn: (r) => r._measurement == "cadena_frio")
  |> filter(fn: (r) => r._field == "temperatura")
```

## Humedad

```flux
from(bucket: "lecturas_iot")
  |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
  |> filter(fn: (r) => r._measurement == "cadena_frio")
  |> filter(fn: (r) => r._field == "humedad")
```

## Último estado NORMAL/ALERTA

```flux
from(bucket: "lecturas_iot")
  |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
  |> filter(fn: (r) => r._measurement == "cadena_frio")
  |> filter(fn: (r) => r._field == "alerta")
  |> last()
```

## Regla de alerta automática

```flux
from(bucket: "lecturas_iot")
  |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
  |> filter(fn: (r) => r._measurement == "cadena_frio")
  |> filter(fn: (r) => r._field == "alerta")
  |> aggregateWindow(every: 5s, fn: max, createEmpty: false)
```

Configuración: ventana de 1 minuto; condición Max > 0; evaluación cada 1 minuto; pending = None; keep firing = None.
