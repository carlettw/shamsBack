"""Yangi (bo'sh) bazada jadvallarni modellardan yaratadi va Alembic'ni 'head' holatiga belgilaydi.

Nega kerak: alembic/versions dagi birinchi migratsiya jadvallarni yaratmaydi
(u mavjud 'payments' jadvalini o'zgartiradi). Shuning uchun bo'sh bazada
`alembic upgrade head` ishlamaydi. Bu skript bir marta ishlatiladi.

Ishga tushirish:  python create_tables.py
"""
from alembic import command
from alembic.config import Config

from sqlalchemy import create_engine

from app.core.config import settings
from app.core.database import Base, _clean_url_for_psycopg2
from app.models import *  # noqa: F401,F403  -- barcha modellarni ro'yxatdan o'tkazadi


def main() -> None:
    # DDL uchun pgbouncer (6543) emas, DIRECT_URL (5432) ishlatiladi
    engine = create_engine(_clean_url_for_psycopg2(settings.DIRECT_URL or settings.DATABASE_URL))
    Base.metadata.create_all(bind=engine)
    print("Jadvallar yaratildi.")
    command.stamp(Config("alembic.ini"), "head")
    print("Alembic 'head' holatiga belgilandi. Tayyor.")


if __name__ == "__main__":
    main()
