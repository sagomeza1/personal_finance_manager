# Bot de Telegram

El bot permite registrar ingresos y gastos directamente desde una conversación de Telegram, sin abrir ninguna interfaz adicional.

## 1. Crear el bot con BotFather

1. Abre Telegram y busca a [@BotFather](https://t.me/BotFather).
2. Envía `/newbot` y sigue las instrucciones (nombre del bot, nombre de usuario terminado en `bot`).
3. BotFather te entregará un **token** con el formato `123456789:ABCdefGhIJKlmNoPQRstuVwxYZ`.

## 2. Configurar el token

Pega el token en tu archivo `.env` (ver [`docs/configuracion.md`](configuracion.md)):

```
FINANCE_BOT_TOKEN=123456789:ABCdefGhIJKlmNoPQRstuVwxYZ
```

## 3. Ejecutar el bot

Con el entorno virtual activado y las variables de entorno cargadas:

```bash
python3 -m finance_app.bot.telegram_bot
```

El bot queda escuchando mensajes (*polling*). Déjalo corriendo en una terminal, `tmux`/`screen`, o como servicio systemd para que funcione de forma continua.

## 4. Comandos disponibles

| Comando | Descripción | Ejemplo |
| --- | --- | --- |
| `/gasto <monto> <categoria> [descripción]` | Registra un gasto | `/gasto 25000 Alimentación Almuerzo` |
| `/ingreso <monto> <categoria> [descripción]` | Registra un ingreso | `/ingreso 2500000 Salario` |
| `/balance [dias]` | Resumen de ingresos, gastos y balance (por defecto 30 días) | `/balance 7` |
| `/recientes [n]` | Últimos N movimientos (por defecto 10) | `/recientes 20` |
| `/ayuda` | Muestra la ayuda con todos los comandos | `/ayuda` |

## 5. Aislamiento de datos por usuario

Cada persona que le escribe al bot tiene sus movimientos completamente separados: internamente se usa el `chat_id` de Telegram como identificador de usuario (`user_id`). Ese mismo `chat_id` es el que debes ingresar en el dashboard (ver [`docs/dashboard.md`](dashboard.md)) para ver tus propios datos.

> Para conocer tu `chat_id`, puedes escribirle a [@userinfobot](https://t.me/userinfobot) en Telegram.
