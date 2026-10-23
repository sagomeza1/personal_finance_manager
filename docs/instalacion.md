# Instalación

## Requisitos

* **Python 3.10 o superior** (desarrollado y probado con Python 3.14).
* **MongoDB** (local o remoto) — ver [`docs/mongodb.md`](mongodb.md) para las opciones disponibles.
* Dependencias Python listadas en `requirements.txt`.

## Clonar el repositorio

```bash
git clone git@github.com:sagomeza1/personal_finance_manager.git
cd personal_finance_manager
```

## Crear entorno virtual e instalar dependencias

```bash
python3 -m venv .venv
source .venv/bin/activate      # en Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

> **Nota (sistemas sin `pip` preinstalado, ej. Ubuntu/Debian recientes):** si `python3 -m venv` falla porque falta `ensurepip`, puedes instalar `pip` manualmente sin tocar el sistema:
> ```bash
> curl -fsSL https://bootstrap.pypa.io/pip/pip.pyz -o /tmp/pip.pyz
> python3 /tmp/pip.pyz install --user -r requirements.txt
> ```

## Variables de entorno

Copia el archivo de ejemplo y complétalo con tus valores reales (ver [`docs/configuracion.md`](configuracion.md)):

```bash
cp .env.example .env
```

Siguiente paso: configura MongoDB ([`docs/mongodb.md`](mongodb.md)) y el bot de Telegram ([`docs/bot-telegram.md`](bot-telegram.md)).
