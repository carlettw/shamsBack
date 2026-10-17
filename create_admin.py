"""Administrator hisobini yaratadi (yoki mavjud foydalanuvchini admin qiladi).

Ishga tushirish:  python create_admin.py
Parol terminalda so'raladi va ekranda ko'rinmaydi.
"""
import getpass
import sys

from app.core.database import SessionLocal
from app.core.security import hash_password
from app.models.user import User, UserRole


def main() -> None:
    email = input("Admin email: ").strip().lower()
    if not email or "@" not in email:
        sys.exit("Email noto'g'ri.")
    full_name = input("To'liq ism [Admin]: ").strip() or "Admin"

    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == email).first()
        if user:
            user.role = UserRole.admin
            db.commit()
            print(f"{email} allaqachon bor edi, endi u admin. Parol o'zgarmadi.")
            return

        password = getpass.getpass("Parol (8-72 belgi): ")
        if not 8 <= len(password) <= 72:
            sys.exit("Parol 8 dan 72 belgigacha bo'lishi kerak.")
        if password != getpass.getpass("Parolni qayta kiriting: "):
            sys.exit("Parollar mos kelmadi.")

        db.add(
            User(
                full_name=full_name,
                email=email,
                hashed_password=hash_password(password),
                role=UserRole.admin,
                preferred_language="uz",
            )
        )
        db.commit()
        print(f"Admin yaratildi: {email}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
