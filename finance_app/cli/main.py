"""CLI local de respaldo para registrar/consultar movimientos sin necesidad del bot de Telegram.

Útil para pruebas rápidas o uso directo desde la terminal de `desk`.

Uso:
    python3 -m finance_app.cli.main gasto <user_id> <monto> <categoria> [descripcion]
    python3 -m finance_app.cli.main ingreso <user_id> <monto> <categoria> [descripcion]
    python3 -m finance_app.cli.main balance <user_id> [dias]
    python3 -m finance_app.cli.main recientes <user_id> [n]
"""
from __future__ import annotations

import sys
from datetime import datetime, timedelta

from finance_app.models.transaction import TransactionType
from finance_app.services.finance_service import FinanceService


def main(argv: list[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    if not argv:
        print(__doc__)
        return 1

    command = argv[0]
    service = FinanceService()

    if command in ("gasto", "ingreso"):
        if len(argv) < 4:
            print(f"Uso: {command} <user_id> <monto> <categoria> [descripcion]")
            return 1
        user_id, amount_s, category = argv[1], argv[2], argv[3]
        description = " ".join(argv[4:])
        try:
            amount = float(amount_s)
            service.register_transaction(
                user_id=user_id,
                type_=TransactionType.GASTO if command == "gasto" else TransactionType.INGRESO,
                amount=amount,
                category=category,
                description=description,
            )
        except ValueError as exc:
            print(f"Error: {exc}")
            return 1
        print(f"OK: {command} de ${amount:,.0f} registrado en '{category.title()}'.")
        return 0

    if command == "balance":
        if len(argv) < 2:
            print("Uso: balance <user_id> [dias]")
            return 1
        user_id = argv[1]
        days = int(argv[2]) if len(argv) > 2 else 30
        start = datetime.now() - timedelta(days=days)
        summary = service.get_balance(user_id, start=start)
        print(f"Balance (últimos {days} días):")
        print(f"  Ingresos: ${summary.total_ingresos:,.0f}")
        print(f"  Gastos  : ${summary.total_gastos:,.0f}")
        print(f"  Balance : ${summary.balance:,.0f}")
        if summary.top_categorias_gasto:
            print("  Top categorías de gasto:")
            for cat in summary.top_categorias_gasto:
                print(f"    - {cat['_id']}: ${cat['total']:,.0f} ({cat['count']} mov.)")
        return 0

    if command == "recientes":
        if len(argv) < 2:
            print("Uso: recientes <user_id> [n]")
            return 1
        user_id = argv[1]
        limit = int(argv[2]) if len(argv) > 2 else 10
        txs = service.list_recent(user_id, limit=limit)
        if not txs:
            print("No hay movimientos registrados.")
            return 0
        for t in txs:
            print(
                f"{t.date.strftime('%Y-%m-%d %H:%M')} | {t.type.value:8s} | "
                f"${t.amount:>12,.0f} | {t.category} | {t.description}"
            )
        return 0

    print(__doc__)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
