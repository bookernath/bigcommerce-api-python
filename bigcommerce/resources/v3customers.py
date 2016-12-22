from .base import *

#
#  Newsletter subscribers
#

class V3NewsletterSubscribers(V3ListableApiResource, V3CreateableApiResource,
                 V3UpdateableApiResource, DeleteableApiResource):
    resource_name = 'v3/customers/subscribers'
