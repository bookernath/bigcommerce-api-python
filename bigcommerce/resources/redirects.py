from .base import *


class Redirects(ListableApiResource, CreateableApiResource,
                UpdateableApiResource, DeleteableApiResource,
                CollectionDeleteableApiResource, CountableApiResource):
    resource_name = 'v2/redirects'
