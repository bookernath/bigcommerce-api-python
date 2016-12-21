from .base import *


class Countries(ListableApiResource, CountableApiResource):
    resource_name = 'v2/countries'

    def states(self, id=None):
        if id:
            return CountryStates.get(self.id, id, connection=self._connection)
        else:
            return CountryStates.all(self.id, connection=self._connection)


class CountryStates(ListableApiSubResource, CountableApiSubResource):
    resource_name = 'states'
    parent_resource = 'v2/countries'
    parent_key = 'country_id'
