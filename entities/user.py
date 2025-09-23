from api.api_manager import ApiManager


class User:
    def __init__(self, email: str, password: str, roles: list[str], api: ApiManager) -> None:
        self.email = email
        self.password = password
        self.roles = roles
        self.api = api  # Сюда будем передавать экземпляр API Manager для запросов

    @property
    def creds(self) -> tuple[str, str]:
        """Возвращает кортеж (email, password)"""
        return self.email, self.password
