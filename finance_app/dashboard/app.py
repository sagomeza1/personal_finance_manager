"""Dashboard interactivo (Streamlit) para visualizar el comportamiento financiero.

Ejecutar con:
    streamlit run finance_app/dashboard/app.py
"""
from __future__ import annotations

import sys
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from finance_app.models.transaction import TransactionType
from finance_app.services.repository import TransactionRepository

st.set_page_config(page_title="Finanzas Personales", page_icon="💰", layout="wide")


@st.cache_resource
def get_repo() -> TransactionRepository:
    return TransactionRepository()


def transactions_to_df(txs) -> pd.DataFrame:
    rows = [
        {
            "Fecha": t.date,
            "Tipo": t.type.value,
            "Monto": t.amount,
            "Categoría": t.category,
            "Descripción": t.description,
        }
        for t in txs
    ]
    return pd.DataFrame(rows)


def main() -> None:
    st.title("💰 Dashboard de Finanzas Personales")

    repo = get_repo()

    with st.sidebar:
        st.header("Filtros")
        user_id = st.text_input(
            "ID de usuario (chat_id de Telegram)",
            value="",
            help="Debe coincidir con el chat_id usado en el bot de Telegram.",
        )
        days = st.slider("Rango de días a analizar", min_value=7, max_value=365, value=30)

    if not user_id:
        st.info("Ingresa tu ID de usuario (chat_id de Telegram) en la barra lateral para ver tus datos.")
        return

    start = datetime.now() - timedelta(days=days)
    txs = repo.list_by_user(user_id, start=start)

    if not txs:
        st.warning("No hay movimientos registrados en este rango de fechas.")
        return

    df = transactions_to_df(txs)

    ingresos = df[df["Tipo"] == TransactionType.INGRESO.value]["Monto"].sum()
    gastos = df[df["Tipo"] == TransactionType.GASTO.value]["Monto"].sum()
    balance = ingresos - gastos

    col1, col2, col3 = st.columns(3)
    col1.metric("Ingresos", f"${ingresos:,.0f}")
    col2.metric("Gastos", f"${gastos:,.0f}")
    col3.metric("Balance", f"${balance:,.0f}", delta=f"{balance:,.0f}")

    st.divider()

    col_a, col_b = st.columns(2)

    with col_a:
        st.subheader("Gastos por categoría")
        gastos_df = df[df["Tipo"] == TransactionType.GASTO.value]
        if not gastos_df.empty:
            by_cat = gastos_df.groupby("Categoría")["Monto"].sum().reset_index()
            fig = px.pie(by_cat, names="Categoría", values="Monto", hole=0.4)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.caption("Sin gastos registrados en este rango.")

    with col_b:
        st.subheader("Evolución diaria (Ingresos vs Gastos)")
        daily = (
            df.assign(Fecha=df["Fecha"].dt.date)
            .groupby(["Fecha", "Tipo"])["Monto"]
            .sum()
            .reset_index()
        )
        fig2 = px.bar(daily, x="Fecha", y="Monto", color="Tipo", barmode="group")
        st.plotly_chart(fig2, use_container_width=True)

    st.divider()
    st.subheader("Historial de movimientos")
    st.dataframe(
        df.sort_values("Fecha", ascending=False),
        use_container_width=True,
        hide_index=True,
    )


if __name__ == "__main__":
    main()
