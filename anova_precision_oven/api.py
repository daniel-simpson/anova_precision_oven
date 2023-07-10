from http.client import responses
from json.decoder import JSONDecodeError
import requests
from websocket import create_connection

from .const import (
    LOGIN_URL,
    APP_ENDPOINT,
    CommandType,
)

from .error import (
    APIError,
    AccessDeniedError,
    OvenUnreachableError
)

class API(object):
    def __init__(self, timeout: int = 10, http_session: requests.Session = None) -> None:
        self._timeout = timeout
        self._http_session = http_session if http_session else requests.Session()
        self.is_authenticated = False

    def login(self, email: str, password: str) -> None:
        response = self._post(
            url = LOGIN_URL,
            json = {
                "email": email,
                "password": password,
                "returnSecureToken": True,
            }
        )
        self.id_token = response.id_token
    
    def _post(
        self,
        path: str,
        payload: dict,
        headers: dict = {},
    ) -> dict:
        try:
            response = self._http_session.post(
                url=self.url(path),
                json=payload,
                timeout=self._timeout,
                headers=headers,
            )
        except (
            requests.exceptions.ConnectionError,
            requests.exceptions.ReadTimeout,
        ) as e:
            raise OvenUnreachableError(e)

        return self._process_response(response)

    def _process_response(self, response: requests.Response) -> dict:
        if(response.status_code >= 400):
           self._handle_error(response)
        
        try:
            response_json = response.json()
        except JSONDecodeError:
            raise APIError(
                "Error while decoding json response: {}".format(response.text)
            )
    
    @staticmethod
    def _handle_error(response: requests.Response) -> None:
        if response.status_code == 404:
            raise APIError(
                "The url {} returned error 404".format(response.request.path_url)
            )

        if response.status_code == 401 or response.status_code == 403:
            response_json = None
            try:
                response_json = response.json()
            except Exception:
                raise AccessDeniedError(response.request.path_url)
            else:
                raise AccessDeniedError(
                    response.request.path_url,
                    response_json.get("error"),
                    response_json.get("message"),
                )

        if response.text is not None and len(response.text) > 0:
            raise APIError(
                "API returned status code '{}: {}' with body: {}".format(
                    response.status_code,
                    responses.get(response.status_code),
                    response.text,
                )
            )
        else:
            raise APIError(
                "API returned status code '{}: {}' ".format(
                    response.status_code, responses.get(response.status_code)
                )
            )
        