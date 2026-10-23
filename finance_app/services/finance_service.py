"""Lógica de negocio: resúmenes financieros, balances y utilidades de análisis."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from finance_app.models.transaction import Transaction, TransactionType
from finance_app.services.repository import TransactionRepository


@dataclass
class BalanceSummary:
    total_ingresos: float
    total_gastos: float
    balance: float
    top_categorias_gasto: List[dict]


class FinanceService:
    """Orquesta operaciones de alto nivel sobre transacciones del usuario."""

    def __init__(self, repo: Optional[TransactionRepository] = None) -> None:
        self.repo = repo or TransactionRepository()

    def register_transaction(
        self,
        user_id: str,
        type_: TransactionType,
        amount: float,
        category: str,
        description: str = "",
        date: Optional[datetime] = None,
    ) -> str:
        if amount <= 0:
            raise ValueError("El monto debe ser mayor a 0")
        tx = Transaction(
            user_id=user_id,
            type=type_,
            amount=amount,
            category=category.strip().title(),
            description=description.strip(),
            date=date or datetime.now(),
        )
        return self.repo.add(tx)

    def get_balance(
        self,
        user_id: str,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
    ) -> BalanceSummary:
        ingresos = self.repo.list_by_user(user_id, start, end, TransactionType.INGRESO)
        gastos = self.repo.list_by_user(user_id, start, end, TransactionType.GASTO)
        total_ingresos = sum(t.amount for t in ingresos)
        total_gastos = sum(t.amount for t in gastos)
        top_gastos = self.repo.summary_by_category(user_id, TransactionType.GASTO, start, end)
        return BalanceSummary(
            total_ingresos=total_ingresos,
            total_gastos=total_gastos,
            balance=total_ingresos - total_gastos,
            top_categorias_gasto=top_gastos[:5],
        )

    def list_recent(self, user_id: str, limit: int = 10) -> List[Transaction]:
        txs = self.repo.list_by_user(user_id)
        return txs[:limit]
