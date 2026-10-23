# Configuración (`.env`)

El archivo `.env` (no versionado en Git) centraliza las credenciales y parámetros de conexión. Parte de la plantilla `.env.example`:

```bash
cp .env.example .env
```

## Variables disponibles

| Variable | Descripción | Valor por defecto |
| --- | --- | --- |
| `FINANCE_BOT_TOKEN` | Token del bot de Telegram (ver [`docs/bot-telegram.md`](bot-telegram.md)) | *(vacío, obligatorio para el bot)* |
| `FINANCE_MONGO_URI` | Cadena de conexión a MongoDB (ver [`docs/mongodb.md`](mongodb.md)) | `mongodb://127.0.0.1:27017/` |
| `FINANCE_DB_NAME` | Nombre de la base de datos a usar dentro de MongoDB | `personal_finance` |

## Cargar las variables antes de ejecutar

En Linux/macOS, exporta las variables del `.env` a tu sesión de terminal antes de correr el bot o el dashboard:

```bash
export $(grep -v '^#' .env | xargs)
```

O, si prefieres no exportarlas manualmente cada vez, instala `python-dotenv` y agrega al inicio de tus scripts `from dotenv import load_dotenv; load_dotenv()` (no incluido por defecto para mantener las dependencias mínimas).

Con las variables configuradas, continúa con:
* [`docs/bot-telegram.md`](bot-telegram.md) — ejecutar el bot de Telegram.
* [`docs/dashboard.md`](dashboard.md) — ejecutar el dashboard visual.
* [`docs/cli.md`](cli.md) — usar la CLI local de respaldo.
