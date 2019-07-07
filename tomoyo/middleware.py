from abc import ABC, abstractmethod


class Middleware(ABC):
    @abstractmethod
    def pre_request(self, request):
        ...

    @abstractmethod
    def post_response(self, response):
        ...
