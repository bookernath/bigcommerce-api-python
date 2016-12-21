from .base import *


class CustomerGroups(ListableApiResource, CreateableApiResource,
                     UpdateableApiResource, DeleteableApiResource,
                     CollectionDeleteableApiResource, CountableApiResource):
    resource_name = 'v2/customer_groups'
