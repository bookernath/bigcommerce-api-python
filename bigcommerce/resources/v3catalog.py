from .base import *


#
#  Products
#

class V3Products(V3ListableApiResource, V3CreateableApiResource,
                 V3UpdateableApiResource, DeleteableApiResource):
    resource_name = 'v3/catalog/products'

    def V3images(self, id=None):
        if id:
            return V3ProductImages.get(self.id, id, connection=self._connection)
        else:
            return V3ProductImages.all(self.id, connection=self._connection)

    def V3options(self, id=None):
        if id:
            return V3ProductOptions.get(self.id, id, connection=self._connection)
        else:
            return V3ProductOptions.all(self.id, connection=self._connection)

    def V3variants(self, id=None):
        if id:
            return V3ProductVariants.get(self.id, id, connection=self._connection)
        else:
            return V3ProductVariants.all(self.id, connection=self._connection)

    def V3modifiers(self, id=None):
        if id:
            return V3ProductModifiers.get(self.id, id, connection=self._connection)
        else:
            return V3ProductModifiers.all(self.id, connection=self._connection)

    def V3complex_rules(self, id=None):
        if id:
            return V3ProductComplexRules.get(self.id, id, connection=self._connection)
        else:
            return V3ProductComplexRules.all(self.id, connection=self._connection)

    def V3videos(self, id=None):
        if id:
            return V3ProductVideos.get(self.id, id, connection=self._connection)
        else:
            return V3ProductVideos.all(self.id, connection=self._connection)


class V3ProductImages(V3ListableApiSubResource, V3CreateableApiSubResource,
                    V3UpdateableApiSubResource, DeleteableApiSubResource):
    resource_name = 'images'
    parent_resource = 'v3/catalog/products'
    parent_key = 'product_id'


class V3ProductOptions(ListableApiSubResource):
    resource_name = 'options'
    parent_resource = 'v3/catalog/products'
    parent_key = 'product_id'


class V3ProductVariants(V3ListableApiSubResource, V3CreateableApiSubResource,
                      V3UpdateableApiSubResource, DeleteableApiSubResource):
    resource_name = 'variants'
    parent_resource = 'v3/catalog/products'
    parent_key = 'product_id'


class V3ProductModifiers(V3ListableApiSubResource, V3CreateableApiSubResource,
                       V3UpdateableApiSubResource, DeleteableApiSubResource):
    resource_name = 'modifiers'
    parent_resource = 'v3/catalog/products'
    parent_key = 'product_id'


class V3ProductComplexRules(V3ListableApiSubResource, V3CreateableApiSubResource,
                          V3UpdateableApiSubResource, DeleteableApiSubResource):
    resource_name = 'complex_rules'
    parent_resource = 'v3/catalog/products'
    parent_key = 'product_id'


class V3ProductVideos(V3ListableApiSubResource, V3CreateableApiSubResource,
                      V3UpdateableApiSubResource, DeleteableApiSubResource):
    resource_name = 'videos'
    parent_resource = 'v3/catalog/products'
    parent_key = 'product_id'


#
#  Variants
#

class V3Variants(V3ListableApiResource, V3CreateableApiResource,
                 V3UpdateableApiResource, DeleteableApiResource):
    resource_name = 'v3/catalog/variants'


#
#  Categories
#

class V3Categories(V3ListableApiResource, V3CreateableApiResource,
                 V3UpdateableApiResource, DeleteableApiResource):
    resource_name = 'v3/catalog/categories'


class V3CategoryTree(V3ListableApiSubResource):
    resource_name = 'tree'
    parent_resource = 'v3/catalog/categories'
    parent_key = None


#
#  Brands
#

class V3Brands(V3ListableApiResource, V3CreateableApiResource,
                 V3UpdateableApiResource, DeleteableApiResource):
    resource_name = 'v3/catalog/brands'


#
#  Catalog Summary
#

class V3CatalogSummary(V3ListableApiResource):
    resource_name = 'v3/catalog/summary'
