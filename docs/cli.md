# CLI local

La CLI es una herramienta de respaldo para registrar o consultar movimientos directamente desde la terminal, sin necesidad de tener el bot de Telegram corriendo. Útil para pruebas rápidas o uso personal en el servidor.

## Uso

Con el entorno virtual activado y las variables de entorno cargadas:

```bash
python3 -m finance_app.cli.main <comando> [argumentos]
```

## Comandos

| Comando | Descripción | Ejemplo |
| --- | --- | --- |
| `gasto <user_id> <monto> <categoria> [descripcion]` | Registra un gasto | `python3 -m finance_app.cli.main gasto mi_id 25000 Alimentacion Almuerzo` |
| `ingreso <user_id> <monto> <categoria> [descripcion]` | Registra un ingreso | `python3 -m finance_app.cli.main ingreso mi_id 2500000 Salario` |
| `balance <user_id> [dias]` | Resumen de balance (por defecto 30 días) | `python3 -m finance_app.cli.main balance mi_id 7` |
| `recientes <user_id> [n]` | Últimos N movimientos (por defecto 10) | `python3 -m finance_app.cli.main recientes mi_id 20` |

## Nota sobre `user_id`

El `user_id` es un identificador libre que tú eliges (puede ser tu nombre, un alias, o el mismo `chat_id` de Telegram si quieres que los datos de la CLI y del bot coincidan — ver [`docs/bot-telegram.md`](bot-telegram.md)).
