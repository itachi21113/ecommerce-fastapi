from app.db.database import SessionLocal
from app.user.model import User
from app.user.roles import UserRole


def create_admin(email: str) -> None:
    db = SessionLocal()

    try:
        user = db.query(User).filter(User.email == email).first()

        if user is None:
            raise ValueError("User not found.")

        user.role = UserRole.ADMIN
        db.commit()

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    create_admin("momo@123.com")