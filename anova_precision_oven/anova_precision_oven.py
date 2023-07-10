from .api import API


class AnovaPrecisionOven:
    def __init__(
            self,
            endpoint: str,
            timeout: int = 10,
        ) -> None:
            self._api = API(
                  endpoint,
                  timeout
            )
    
    def login(
            self,
            email: str,
            password: str,
        ) -> None:
          self._api.login(email, password)