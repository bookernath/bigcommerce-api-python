class Mapping(dict):
    """
    Mapping

    provides '.' access to dictionary keys
    """
    def __init__(self, mapping, *args, **kwargs):
        """
        Create a new mapping. Filters the mapping argument
        to remove any elements that are already methods on the
        object.

        For example, Orders retains its `coupons` method, instead
        of being replaced by the dict describing the coupons endpoint
        """
        filter_args = {k: mapping[k] for k in mapping if k not in dir(self)}
        self.__dict__ = self
        dict.__init__(self, filter_args, *args, **kwargs)

    def __str__(self):
        """
        Display as a normal dict, but filter out underscored items first
        """
        return str({k: self.__dict__[k] for k in self.__dict__ if not k.startswith("_")})

    def __repr__(self):
        return "<%s at %s, %s>" % (type(self).__name__, hex(id(self)), str(self))


#
#  V2 Methods
#


class ApiResource(Mapping):
    resource_name = ""  # The identifier which describes this resource in urls

    @classmethod
    def _create_object(cls, response, connection=None):
        if isinstance(response, list):
            return [cls._create_object(obj, connection) for obj in response]
        else:
            return cls(response, _connection=connection)

    @classmethod
    def _make_request(cls, method, url, connection, data=None, params={}, headers={}):
        return connection.make_request(method, url, data, params, headers)

    @classmethod
    def _get_path(cls, id):
        return "%s/%s" % (cls.resource_name, id)

    @classmethod
    def get(cls, id, connection=None, **params):
        response = cls._make_request('GET', cls._get_path(id), connection, params=params)
        return cls._create_object(response, connection=connection)


class ApiSubResource(ApiResource):
    parent_resource = ""
    parent_key = ""

    @classmethod
    def _get_path(cls, id, parentid):
        return "%s/%s/%s/%s" % (cls.parent_resource, parentid, cls.resource_name, id)

    @classmethod
    def get(cls, parentid, id, connection=None, **params):
        response = cls._make_request('GET', cls._get_path(id, parentid), connection, params=params)
        return cls._create_object(response, connection=connection)

    def parent_id(self):
        return self[self.parent_key]


class CreateableApiResource(ApiResource):
    @classmethod
    def _create_path(cls):
        return cls.resource_name

    @classmethod
    def create(cls, connection=None, **params):
        response = cls._make_request('POST', cls._create_path(), connection, data=params)
        return cls._create_object(response, connection=connection)


class CreateableApiSubResource(ApiSubResource):
    @classmethod
    def _create_path(cls, parentid):
        return "%s/%s/%s" % (cls.parent_resource, parentid, cls.resource_name)

    @classmethod
    def create(cls, parentid, connection=None, **params):
        response = cls._make_request('POST', cls._create_path(parentid), connection, data=params)
        return cls._create_object(response, connection=connection)


class ListableApiResource(ApiResource):
    @classmethod
    def _get_all_path(cls):
        return cls.resource_name

    @classmethod
    def all(cls, connection=None, **params):
        request = cls._make_request('GET', cls._get_all_path(), connection, params=params)
        return cls._create_object(request, connection=connection)


class ListableApiSubResource(ApiSubResource):
    @classmethod
    def _get_all_path(cls, parentid=None):
        # Not all sub resources require a parent id.  Eg: /api/v2/products/skus?sku=<value>
        if (parentid):
            return "%s/%s/%s" % (cls.parent_resource, parentid, cls.resource_name)
        else: 
            return "%s/%s" % (cls.parent_resource, cls.resource_name)

    @classmethod
    def all(cls, parentid=None, connection=None, **params):
        response = cls._make_request('GET', cls._get_all_path(parentid), connection, params=params)
        return cls._create_object(response, connection=connection)


class UpdateableApiResource(ApiResource):
    def _update_path(self):
        return "%s/%s" % (self.resource_name, self.id)

    def update(self, **updates):
        response = self._make_request('PUT', self._update_path(), self._connection, data=updates)
        return self._create_object(response, connection=self._connection)


class UpdateableApiSubResource(ApiSubResource):
    def _update_path(self):
        return "%s/%s/%s/%s" % (self.parent_resource, self.parent_id(), self.resource_name, self.id)

    def update(self, **updates):
        response = self._make_request('PUT', self._update_path(), self._connection, data=updates)
        return self._create_object(response, connection=self._connection)


class DeleteableApiResource(ApiResource):
    def _delete_path(self):
        return "%s/%s" % (self.resource_name, self.id)

    def delete(self):
        return self._make_request('DELETE', self._delete_path(), self._connection)


class DeleteableApiSubResource(ApiSubResource):
    def _delete_path(self):
        return "%s/%s/%s/%s" % (self.parent_resource, self.parent_id(), self.resource_name, self.id)

    def delete(self):
        return self._make_request('DELETE', self._delete_path(), self._connection)


class CollectionDeleteableApiResource(ApiResource):
    @classmethod
    def _delete_all_path(cls):
        return cls.resource_name

    @classmethod
    def delete_all(cls, connection=None):
        return cls._make_request('DELETE', cls._delete_all_path(), connection)


class CollectionDeleteableApiSubResource(ApiSubResource):
    @classmethod
    def _delete_all_path(cls, parentid):
        return "%s/%s/%s" % (cls.parent_resource, parentid, cls.resource_name)

    @classmethod
    def delete_all(cls, parentid, connection=None):
        return cls._make_request('DELETE', cls._delete_all_path(parentid), connection)


class CountableApiResource(ApiResource):
    @classmethod
    def _count_path(cls):
        return "%s/count" % (cls.resource_name)

    @classmethod
    def count(cls, connection=None, **params):
        response = cls._make_request('GET', cls._count_path(), connection, params=params)
        return response['count']


class CountableApiSubResource(ApiSubResource):
    # Account for the fairly common case where the count path doesn't include the parent id
    count_resource = None

    @classmethod
    def _count_path(cls, parentid=None):
        if parentid is not None:
            return "%s/%s/%s/count" % (cls.parent_resource, parentid, cls.resource_name)
        elif cls.count_resource is not None:
            return "%s/count" % (cls.count_resource)
        else:
            # misconfiguration
            raise NotImplementedError('Count not implemented for this resource.')

    @classmethod
    def count(cls, parentid=None, connection=None, **params):
        response = cls._make_request('GET', cls._count_path(parentid), connection, params=params)
        return response['count']


#
#  V3 methods
#

class AttrList(list):
    """
    A subclass of list that can accept additional attributes, enabling us to put metadata on the list.
    Should be able to be used just like a regular list.                                   # [2]
    """
    def __new__(self, *args, **kwargs):
        return super(AttrList, self).__new__(self, args, kwargs)

    def __init__(self, *args, **kwargs):
        if len(args) == 1 and hasattr(args[0], '__iter__'):
            list.__init__(self, args[0])
        else:
            list.__init__(self, args)
        self.__dict__.update(kwargs)

    def __call__(self, **kwargs):
        self.__dict__.update(kwargs)
        return self


class V3ApiResource(ApiResource):
    @classmethod
    def _create_object(cls, response, connection=None):
        if isinstance(response, list):
            return AttrList(cls._create_object(obj, connection) for obj in response)
        else:
            return cls(response, _connection=connection)

    @classmethod
    def get(cls, id, connection=None, **params):
        response = cls._make_request('GET', cls._get_path(id), connection, params=params)
        object = cls._create_object(response['data'], connection=connection)
        object.meta = response['meta']
        return object


class V3ApiSubResource(ApiSubResource):
    @classmethod
    def get(cls, parentid, id, connection=None, **params):
        response = cls._make_request('GET', cls._get_path(id, parentid), connection, params=params)
        object = cls._create_object(response['data'], connection=connection)
        object.meta = response['meta']
        return object


class V3CreateableApiResource(V3ApiResource):
    @classmethod
    def create(cls, connection=None, **params):
        response = cls._make_request('POST', cls._create_path(), connection, data=params)
        object = cls._create_object(response['data'], connection=connection)
        object.meta = response['meta']
        return object


class V3CreateableApiSubResource(V3ApiSubResource):
    @classmethod
    def create(cls, parentid, connection=None, **params):
        response = cls._make_request('POST', cls._create_path(parentid), connection, data=params)
        object = cls._create_object(response['data'], connection=connection)
        object.meta = response['meta']
        return object


class V3ListableApiResource(V3ApiResource):
    @classmethod
    def _get_all_path(cls):
        return cls.resource_name

    @classmethod
    def all(cls, connection=None, auto_paginate=False, **params):
        if auto_paginate:
            collection = cls.auto_paginate(connection, **params)
        else:
            data = cls._make_request('GET', cls._get_all_path(), connection, params=params)
            collection = cls._create_object(data['data'], connection=connection)
            collection.meta = data['meta']
        return collection

    # Very basic auto-pagination, use at your own risk!
    @classmethod
    def auto_paginate(cls, connection=None, **params):
        if not params.get('page'):
            params['page'] = 1
        request = cls._make_request('GET', cls._get_all_path(), connection, params=params)
        collection = AttrList(request['data'])

        # If a "next page" is listed in the response meta, increment page by 1 and add the results to the collection

        next = request['meta']['pagination'].get('links', {}).get('next')
        while bool(next):
            params['page'] += 1
            next_page = cls._make_request('GET', cls._get_all_path(), connection, params=params)
            collection += next_page['data']
            next = next_page['meta'].get('pagination', {}).get('links', {}).get('next')

        # Add our own meta object mirroring the API response which has the total number of objects
        # reported by the API as well as the total we actually fetched which may differ when starting page > 1
        # It may also differ if the download takes a long time and the data is changing!
        collection.meta = dict(pagination=dict(total=request['meta']['pagination']['total'],
                                               count=len(collection)))
        return collection


class V3ListableApiSubResource(V3ApiSubResource):
    @classmethod
    def _get_all_path(cls, parentid=None):
        # Not all sub resources require a parent id.  Eg: /api/v2/products/skus?sku=<value>
        if (parentid):
            return "%s/%s/%s" % (cls.parent_resource, parentid, cls.resource_name)
        else:
            return "%s/%s" % (cls.parent_resource, cls.resource_name)

    @classmethod
    def all(cls, parentid=None, connection=None, auto_paginate=False, **params):
        if auto_paginate:
            collection = cls.auto_paginate(connection, **params)
        else:
            response = cls._make_request('GET', cls._get_all_path(parentid), connection, params=params)
            collection = cls._create_object(response['data'], connection=connection)
            collection.meta = response['meta']
        return collection

    @classmethod
    def auto_paginate(cls, parentid=None, connection=None, **params):
        if not params.get('page'):
            params['page'] = 1
        request = cls._make_request('GET', cls._get_all_path(), connection, params=params)
        collection = AttrList(request['data'])

        # If a "next page" is listed in the response meta, increment page by 1 and add the results to the collection

        next = request['meta']['pagination'].get('links', {}).get('next')
        while bool(next):
            params['page'] += 1
            next_page = cls._make_request('GET', cls._get_all_path(parentid), connection, params=params)
            collection += next_page['data']
            next = next_page['meta'].get('pagination', {}).get('links', {}).get('next')

        # Add our own meta object mirroring the API response which has the total number of objects
        # reported by the API as well as the total we actually fetched which may differ when starting page > 1
        # It may also differ if the download takes a long time and the data is changing!
        collection.meta = dict(pagination=dict(total=request['meta']['pagination']['total'],
                                               count=len(collection)))
        return collection


class V3UpdateableApiResource(V3ApiResource):
    def _update_path(self):
        return "%s/%s" % (self.resource_name, self.id)

    def update(self, **updates):
        response = self._make_request('PUT', self._update_path(), self._connection, data=updates)
        object = self._create_object(response['data'], connection=self._connection)
        object.meta = response['meta']
        return object


class V3UpdateableApiSubResource(V3ApiSubResource):
    def _update_path(self):
        return "%s/%s/%s/%s" % (self.parent_resource, self.parent_id(), self.resource_name, self.id)

    def update(self, **updates):
        response = self._make_request('PUT', self._update_path(), self._connection, data=updates)
        object = self._create_object(response['data'], connection=self._connection)
        object.meta = response['meta']
        return object
