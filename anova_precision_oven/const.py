from enum import Enum

LOGIN_URL = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=AIzaSyCGJwHXUhkNBdPkH3OAkjc9-3xMMjvanfU"
APP_ENDPOINT = "wss://app.oven.anovaculinary.io"

class CommandType(Enum):
    AUTH = "AUTH_TOKEN"
