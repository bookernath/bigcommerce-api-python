from .base import *


class Webhooks(ListableApiResource, CreateableApiResource,
               UpdateableApiResource, DeleteableApiResource):
    resource_name = 'v2/hooks'
