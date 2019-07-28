from abc import ABC, abstractmethod
import json
from http import HTTPStatus

from .net import HttpHeader
from .request import Request


class ResponseBase(ABC):
    @property
    @abstractmethod
    def status(self) -> HTTPStatus:
        ...

    @property
    def status_code_message(self) -> str:
        if not hasattr(self, '_status_code_message'):
            formatted = " ".join((s.capitalize() for s in self.status.name.split("_")))
            self._status_code_message = f"{self.status.value} {formatted}"
        return self._status_code_message

    def __init__(self, headers: HttpHeader, body):
        self.headers = headers
        self.body = body


class ErrorResponseBase(ResponseBase):
    headers = HttpHeader(content_type="text/plain")

    def __init__(self):
        super().__init__(self.headers, self.status_code_message)



class NotFound(ErrorResponseBase):
    status = HTTPStatus.NOT_FOUND


class MethodNotAllowed(ErrorResponseBase):
    status = HTTPStatus.METHOD_NOT_ALLOWED


class OK(ResponseBase):
    status = HTTPStatus.OK
    def __init__(self, headers, body):
        super().__init__(headers, body)


def build_ok_response(response_body):
    content_type = "text/plain"
    if isinstance(response_body, dict):
        response_body = json.dumps(response_body)
        content_type = "application/json"
    return OK(
        HttpHeader(content_type=content_type, content_length=str(len(response_body))),
        response_body,
    )

