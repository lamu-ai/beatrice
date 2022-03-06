#!/usr/bin/env sh

python -m app.prestart
alembic upgrade head
python -m app.init
uvicorn app.main:app --reload --workers 1 --host 0.0.0.0 --port 8000
