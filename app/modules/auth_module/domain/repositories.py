from abc import ABC, abstractmethod
from app.modules.auth_module.domain.models import User


class UserRepository(ABC):
    @abstractmethod
    def get_by_username(self, username: str) -> User | None:
        raise NotImplementedError
