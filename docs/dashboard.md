# Dashboard

El dashboard es una aplicación web (Streamlit) para visualizar el comportamiento financiero a lo largo del tiempo: balance, gastos por categoría y evolución diaria.

## Ejecutar

Con el entorno virtual activado y las variables de entorno cargadas (ver [`docs/configuracion.md`](configuracion.md)):

```bash
streamlit run finance_app/dashboard/app.py
```

Esto abre el dashboard en tu navegador, normalmente en `http://localhost:8501`.

## Uso

1. En la barra lateral, ingresa tu **ID de usuario** (el mismo `chat_id` de Telegram que usas con el bot — ver [`docs/bot-telegram.md`](bot-telegram.md)).
2. Ajusta el **rango de días** a analizar con el control deslizante.
3. El dashboard muestra:
   * **Métricas principales:** ingresos, gastos y balance del período.
   * **Gastos por categoría:** gráfico de pastel.
   * **Evolución diaria:** gráfico de barras comparando ingresos vs. gastos día a día.
   * **Historial completo:** tabla con todos los movimientos del período, ordenados por fecha.

## Acceso remoto (opcional)

Por defecto, Streamlit solo escucha en `localhost`. Para acceder desde otro dispositivo en tu red local:

```bash
streamlit run finance_app/dashboard/app.py --server.address 0.0.0.0
```

> Si expones el dashboard fuera de tu red local, asegúrate de agregar autenticación adicional — Streamlit no incluye login por defecto.
