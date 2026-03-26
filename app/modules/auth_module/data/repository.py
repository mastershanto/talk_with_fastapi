from app.modules.auth_module.domain.models import User


class DummyUserRepository:
    def get_by_username(self, username: str) -> User | None:
        return User(id=1, username=username)
