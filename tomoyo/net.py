import enum


class HttpHeader(dict):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def as_key_value_pairs(self):
        return [
            ("-".join(s.capitalize() for s in k.split("_")), v) for k, v in self.items()
        ]


class HttpMethod(enum.Enum):
    GET = "get"
    POST = "post"
    PUT = "put"
    DELETE = "delete"
