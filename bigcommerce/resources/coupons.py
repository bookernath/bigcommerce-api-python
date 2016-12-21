from .base import *


class Coupons(ListableApiResource, CreateableApiResource,
              UpdateableApiResource, DeleteableApiResource,
              CollectionDeleteableApiResource, CountableApiResource):
    resource_name = 'v2/coupons'
