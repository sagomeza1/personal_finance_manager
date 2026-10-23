# Personal Finance Manager

Herramienta para el seguimiento de finanzas personales: registra ingresos y gastos desde un **bot de Telegram**, consulta y edita datos desde una **CLI local**, y visualiza tu comportamiento financiero en un **dashboard interactivo**. Todo respaldado por **MongoDB**.

## Inicio rápido

```bash
git clone git@github.com:sagomeza1/personal_finance_manager.git
cd personal_finance_manager
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # completa tus credenciales (ver docs/configuracion.md)
```

## Documentación

| Guía | Contenido |
| --- | --- |
| [`docs/instalacion.md`](docs/instalacion.md) | Requisitos e instalación detallada |
| [`docs/mongodb.md`](docs/mongodb.md) | Opciones para levantar MongoDB (local, sistema, Atlas) |
| [`docs/configuracion.md`](docs/configuracion.md) | Variables de entorno (`.env`) |
| [`docs/bot-telegram.md`](docs/bot-telegram.md) | Crear y ejecutar el bot de Telegram, comandos disponibles |
| [`docs/dashboard.md`](docs/dashboard.md) | Ejecutar y usar el dashboard visual (Streamlit) |
| [`docs/cli.md`](docs/cli.md) | Uso de la CLI local de respaldo |

## Licencia

Repositorio personal de Alejandro Gómez.
