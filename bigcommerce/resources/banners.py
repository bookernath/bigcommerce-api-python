from .base import *


class Banners(ListableApiResource, CreateableApiResource,
              UpdateableApiResource, DeleteableApiResource,
              CollectionDeleteableApiResource):
    resource_name = 'v2/banners'
