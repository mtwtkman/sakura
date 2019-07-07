class ReservedPathError(Exception):
    pass


class Service:
    def __init__(self):
        self.resource_map = {}

    def service(self, resource):
        if resource.path in self.resource_map:
            raise ReservedPathError(resource.path)
        self.resource_map[resource.path] = resource
        return self
