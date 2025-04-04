from enum import Enum


class APIRoutes(str, Enum):
    VALIDATE_DATA = "/api/data"
    GET_RESULT = "/api/result"

    def __str__(self):
        return self.value
