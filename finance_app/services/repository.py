"""Capa de acceso a datos: conexión a MongoDB y repositorios de Transacciones/Deudas."""
from __future__ import annotations

import os
from datetime import datetime
from typing import Iterable, List, Optional

from pymongo import MongoClient
from pymongo.collection import Collection

from finance_app.models.transaction import Debt, Transaction, TransactionType

MONGO_URI = os.environ.get("FINANCE_MONGO_URI", "mongodb://127.0.0.1:27017/")
DB_NAME = os.environ.get("FINANCE_DB_NAME", "personal_finance")


def get_client() -> MongoClient:
    return MongoClient(MONGO_URI)


def get_db(client: Optional[MongoClient] = None):
    client = client or get_client()
    return client[DB_NAME]


class TransactionRepository:
    """Repositorio CRUD de transacciones (ingresos/gastos) sobre MongoDB."""

    def __init__(self, client: Optional[MongoClient] = None) -> None:
        self.client = client or get_client()
        self.collection: Collection = get_db(self.client)["transactions"]
        self.collection.create_index([("user_id", 1), ("date", -1)])

    def add(self, transaction: Transaction) -> str:
        result = self.collection.insert_one(transaction.to_dict())
        return str(result.inserted_id)

    def list_by_user(
        self,
        user_id: str,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
        type_: Optional[TransactionType] = None,
    ) -> List[Transaction]:
        query: dict = {"user_id": user_id}
        if start or end:
            query["date"] = {}
            if start:
                query["date"]["$gte"] = start
            if end:
                query["date"]["$lte"] = end
        if type_:
            query["type"] = type_.value
        docs = self.collection.find(query).sort("date", -1)
        return [Transaction.from_dict(d) for d in docs]

    def delete(self, transaction_id: str) -> bool:
        from bson import ObjectId

        result = self.collection.delete_one({"_id": ObjectId(transaction_id)})
        return result.deleted_count > 0

    def summary_by_category(
        self,
        user_id: str,
        type_: TransactionType,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
    ) -> List[dict]:
        match: dict = {"user_id": user_id, "type": type_.value}
        if start or end:
            match["date"] = {}
            if start:
                match["date"]["$gte"] = start
            if end:
                match["date"]["$lte"] = end
        pipeline = [
            {"$match": match},
            {"$group": {"_id": "$category", "total": {"$sum": "$amount"}, "count": {"$sum": 1}}},
            {"$sort": {"total": -1}},
        ]
        return list(self.collection.aggregate(pipeline))


class DebtRepository:
    """Repositorio CRUD de deudas sobre MongoDB."""

    def __init__(self, client: Optional[MongoClient] = None) -> None:
        self.client = client or get_client()
        self.collection: Collection = get_db(self.client)["debts"]
        self.collection.create_index([("user_id", 1)])

    def add(self, debt: Debt) -> str:
        result = self.collection.insert_one(debt.to_dict())
        return str(result.inserted_id)

    def list_by_user(self, user_id: str) -> List[Debt]:
        docs = self.collection.find({"user_id": user_id})
        return [Debt.from_dict(d) for d in docs]

    def update_remaining(self, debt_id: str, new_remaining: float) -> bool:
        from bson import ObjectId

        result = self.collection.update_one(
            {"_id": ObjectId(debt_id)}, {"$set": {"remaining_amount": new_remaining}}
        )
        return result.modified_count > 0

    def delete(self, debt_id: str) -> bool:
        from bson import ObjectId

        result = self.collection.delete_one({"_id": ObjectId(debt_id)})
        return result.deleted_count > 0
