from .base import *


class Currencies(ListableApiResource, CreateableApiResource,
              UpdateableApiResource, DeleteableApiResource):
    resource_name = 'v2/currencies'
