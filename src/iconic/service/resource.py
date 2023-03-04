from iconic.model.resource import Resource
from iconic.service.base import BaseService


class ResourceService(BaseService):
    def __init__(self):
        super().__init__()

    def get_resource(self, resource_name: str) -> Resource:
        return self.db.get(Resource, resource_name)
