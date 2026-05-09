# CLAUDE.md — Real Estate SaaS

## المشروع
CRM عقاري للوكلاء الأفراد — FastAPI + PostgreSQL + Redis

## Stack
- FastAPI (async) + SQLAlchemy 2.0 (async) + Alembic
- PostgreSQL + Redis + Celery
- pytest + httpx للـ tests

## قواعد صارمة
- tenant_id في كل query — بدون استثناء
- Routes → Services → Models (لا تتجاوز)
- Type hints في كل مكان
- لا secrets في الكود

## أوامر التشغيل
- dev: uvicorn app.main:app --reload
- tests: pytest -v -x
- migration: alembic revision --autogenerate -m "desc"
- apply: alembic upgrade head

## Models الموجودة
- Tenant (مكتمل)
- Client (التالي)
- Property (التالي)
- Deal (التالي)