"""Bot de Telegram para registrar ingresos/gastos rápidamente por chat.

Uso de comandos:
  /gasto <monto> <categoria> [descripción]   -> registra un gasto
  /ingreso <monto> <categoria> [descripción] -> registra un ingreso
  /balance [dias]                             -> resumen de balance (por defecto 30 días)
  /recientes [n]                              -> últimos N movimientos (por defecto 10)
  /ayuda                                       -> muestra esta ayuda

El identificador de usuario financiero (`user_id`) se deriva del chat_id de
Telegram, de modo que cada persona que hable con el bot lleva su propio
registro, aislado del resto.
"""
from __future__ import annotations

import logging
import os
from datetime import datetime, timedelta

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from finance_app.models.transaction import TransactionType
from finance_app.services.finance_service import FinanceService

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

BOT_TOKEN = os.environ.get("FINANCE_BOT_TOKEN", "")

HELP_TEXT = (
    "💰 *Bot de Finanzas Personales*\n\n"
    "/gasto <monto> <categoria> [descripción] — registrar un gasto\n"
    "  Ej: `/gasto 25000 Alimentación Almuerzo`\n\n"
    "/ingreso <monto> <categoria> [descripción] — registrar un ingreso\n"
    "  Ej: `/ingreso 2500000 Salario`\n\n"
    "/balance [dias] — resumen de balance (por defecto últimos 30 días)\n"
    "/recientes [n] — últimos N movimientos (por defecto 10)\n"
    "/ayuda — muestra este mensaje"
)


def _user_id(update: Update) -> str:
    return str(update.effective_chat.id)


def _service() -> FinanceService:
    return FinanceService()


async def cmd_ayuda(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_markdown(HELP_TEXT)


async def _registrar(update: Update, context: ContextTypes.DEFAULT_TYPE, type_: TransactionType) -> None:
    args = context.args
    if len(args) < 2:
        await update.message.reply_text(
            f"Formato: /{type_.value} <monto> <categoria> [descripción]"
        )
        return
    try:
        amount = float(args[0])
    except ValueError:
        await update.message.reply_text("El monto debe ser un número (ej. 25000).")
        return

    category = args[1]
    description = " ".join(args[2:]) if len(args) > 2 else ""

    service = _service()
    try:
        service.register_transaction(
            user_id=_user_id(update),
            type_=type_,
            amount=amount,
            category=category,
            description=description,
        )
    except ValueError as exc:
        await update.message.reply_text(f"Error: {exc}")
        return

    emoji = "💸" if type_ == TransactionType.GASTO else "💵"
    await update.message.reply_text(
        f"{emoji} Registrado: ${amount:,.0f} en '{category.title()}'"
        + (f" ({description})" if description else "")
    )


async def cmd_gasto(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await _registrar(update, context, TransactionType.GASTO)


async def cmd_ingreso(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await _registrar(update, context, TransactionType.INGRESO)


async def cmd_balance(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    days = 30
    if context.args:
        try:
            days = int(context.args[0])
        except ValueError:
            pass

    service = _service()
    start = datetime.now() - timedelta(days=days)
    summary = service.get_balance(_user_id(update), start=start)

    lines = [
        f"📊 *Balance (últimos {days} días)*",
        f"Ingresos: ${summary.total_ingresos:,.0f}",
        f"Gastos: ${summary.total_gastos:,.0f}",
        f"Balance: ${summary.balance:,.0f}",
    ]
    if summary.top_categorias_gasto:
        lines.append("\n*Top categorías de gasto:*")
        for cat in summary.top_categorias_gasto:
            lines.append(f"  • {cat['_id']}: ${cat['total']:,.0f} ({cat['count']} mov.)")

    await update.message.reply_markdown("\n".join(lines))


async def cmd_recientes(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    limit = 10
    if context.args:
        try:
            limit = int(context.args[0])
        except ValueError:
            pass

    service = _service()
    txs = service.list_recent(_user_id(update), limit=limit)
    if not txs:
        await update.message.reply_text("No hay movimientos registrados todavía.")
        return

    lines = [f"🧾 *Últimos {len(txs)} movimientos:*"]
    for t in txs:
        emoji = "💸" if t.type == TransactionType.GASTO else "💵"
        lines.append(
            f"{emoji} {t.date.strftime('%Y-%m-%d')} — ${t.amount:,.0f} "
            f"[{t.category}]" + (f" {t.description}" if t.description else "")
        )
    await update.message.reply_markdown("\n".join(lines))


def build_application() -> Application:
    if not BOT_TOKEN:
        raise RuntimeError(
            "Falta configurar la variable de entorno FINANCE_BOT_TOKEN con el token del bot de Telegram."
        )
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("ayuda", cmd_ayuda))
    application.add_handler(CommandHandler("start", cmd_ayuda))
    application.add_handler(CommandHandler("gasto", cmd_gasto))
    application.add_handler(CommandHandler("ingreso", cmd_ingreso))
    application.add_handler(CommandHandler("balance", cmd_balance))
    application.add_handler(CommandHandler("recientes", cmd_recientes))
    return application


def main() -> None:
    app = build_application()
    logger.info("Bot de finanzas personales iniciado. Esperando mensajes...")
    app.run_polling()


if __name__ == "__main__":
    main()
