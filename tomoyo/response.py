from http import HTTPStatus

from .net import HttpHeader
from .request import Request



def http_status_code_message(status):
    formatted = " ".join((s.capitalize() for s in status.name.split("_")))
    return f"{status.value} {formatted}"


class Response():
    def __init__(self, headers, status, body):
        self.headers = headers
        self.status = status
        self.status_code_message = http_status_code_message(status)
        self.body = body


def _build_template_response(status):
    body = http_status_code_message(status)
    headers = HttpHeader(content_type="text/plain", content_rength=str(len(body)))
    return Response(headers, status, body)


def build_not_found_response():
    return _build_template_response(HTTPStatus.NOT_FOUND)


def build_method_not_allowed_response():
    return _build_template_response(HTTPStatus.METHOD_NOT_ALLOWED)


def build_ok_response(response_body):
    content_type = "text/plain"
    if isinstance(response_body, dict):
        response_body = json.dumps(response_body)
        content_type = "application/json"
    return Response(
        HttpHeader(content_type=content_type, content_length=str(len(response_body))),
        HTTPStatus.OK,
        response_body,
    )
