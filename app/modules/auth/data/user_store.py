from app.core.security import hash_password
from app.modules.auth.domain.models import UserInDB


fake_users_db: dict[str, UserInDB] = {
    "alice": UserInDB(
        username="alice",
        full_name="Alice Example",
        email="alice@example.com",
        disabled=False,
        hashed_password=hash_password("password123"),
    )
}


def get_user(username: str) -> UserInDB | None:
    user = fake_users_db.get(username)
    return user
