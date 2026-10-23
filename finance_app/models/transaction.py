"""Modelos de datos para transacciones financieras personales."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


class TransactionType(str, Enum):
    INGRESO = "ingreso"
    GASTO = "gasto"


# Categorías por defecto sugeridas. El usuario puede usar cualquier texto libre,
# pero estas sirven como catálogo de referencia para el bot y el dashboard.
DEFAULT_EXPENSE_CATEGORIES = [
    "Vivienda", "Alimentación", "Transporte", "Servicios", "Salud",
    "Educación", "Entretenimiento", "Deudas", "Ahorro/Inversión", "Otros",
]
DEFAULT_INCOME_CATEGORIES = [
    "Salario", "Freelance", "Inversiones", "Regalo", "Otros",
]


@dataclass
class Transaction:
    """Representa un movimiento financiero individual (ingreso o gasto)."""

    user_id: str
    type: TransactionType
    amount: float
    category: str
    description: str = ""
    date: datetime = field(default_factory=datetime.now)
    id: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "user_id": self.user_id,
            "type": self.type.value,
            "amount": self.amount,
            "category": self.category,
            "description": self.description,
            "date": self.date,
        }

    @staticmethod
    def from_dict(data: dict) -> "Transaction":
        return Transaction(
            id=str(data.get("_id")) if data.get("_id") is not None else None,
            user_id=data["user_id"],
            type=TransactionType(data["type"]),
            amount=float(data["amount"]),
            category=data["category"],
            description=data.get("description", ""),
            date=data["date"] if isinstance(data["date"], datetime) else datetime.fromisoformat(data["date"]),
        )


@dataclass
class Debt:
    """Representa una deuda u obligación financiera a hacerle seguimiento."""

    user_id: str
    name: str
    total_amount: float
    remaining_amount: float
    monthly_payment: float = 0.0
    interest_rate: float = 0.0
    due_day: Optional[int] = None  # día del mes en que vence la cuota
    notes: str = ""
    id: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "user_id": self.user_id,
            "name": self.name,
            "total_amount": self.total_amount,
            "remaining_amount": self.remaining_amount,
            "monthly_payment": self.monthly_payment,
            "interest_rate": self.interest_rate,
            "due_day": self.due_day,
            "notes": self.notes,
        }

    @staticmethod
    def from_dict(data: dict) -> "Debt":
        return Debt(
            id=str(data.get("_id")) if data.get("_id") is not None else None,
            user_id=data["user_id"],
            name=data["name"],
            total_amount=float(data["total_amount"]),
            remaining_amount=float(data["remaining_amount"]),
            monthly_payment=float(data.get("monthly_payment", 0.0)),
            interest_rate=float(data.get("interest_rate", 0.0)),
            due_day=data.get("due_day"),
            notes=data.get("notes", ""),
        )
