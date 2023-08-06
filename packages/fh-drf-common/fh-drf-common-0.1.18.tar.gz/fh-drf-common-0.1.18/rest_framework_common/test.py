from mock import patch
import datetime
import inspect
import json
import os
import platform

from django.conf import settings
from django.test.client import ClientHandler
from freezegun import freeze_time as fg_freeze_time
from freezegun.api import FakeDatetime
from google.appengine.api import datastore_types
from google.appengine.ext import ndb
from google.appengine.ext import testbed
from jsonschema import Draft4Validator
from rest_framework import status
from rest_framework.test import APITestCase

import sendsms

_is_cpython = (
    hasattr(platform, 'python_implementation') and
    platform.python_implementation().lower() == "cpython"
)


# Need any async tasklets to run before request is complete since
# Django tests don't run through real wsgi handler we fake it here.
old_get_response = ClientHandler.get_response
@ndb.toplevel
def get_response(self, *args, **kwargs):
    return old_get_response(self, *args, **kwargs)
ClientHandler.get_response = get_response


class HTTPStatusTestCaseMixin(object):

    def assertHTTP200(self, response):
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def assertHTTP201(self, response):
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def assertHTTP204(self, response):
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def assertHTTP400(self, response):
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def assertHTTP401(self, response):
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def assertHTTP403(self, response):
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def assertHTTP404(self, response):
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class _freeze_time(object):
    def __init__(self, *args, **kwargs):
        self._gae_patch = patch('google.appengine.ext.db.DateTimeProperty.data_type', new=FakeDatetime)
        self._freeze = fg_freeze_time(*args, **kwargs)
        datastore_types._VALIDATE_PROPERTY_VALUES[FakeDatetime] = datastore_types.ValidatePropertyNothing
        datastore_types._PACK_PROPERTY_VALUES[FakeDatetime] = datastore_types.PackDatetime
        datastore_types._PROPERTY_MEANINGS[FakeDatetime] = datastore_types.entity_pb.Property.GD_WHEN

    def __call__(self, func):
        if inspect.isclass(func):
            return self._freeze.decorate_class(func)
        return self._freeze.decorate_callable(func)

    def start(self):
        self._freeze.start()
        self._gae_patch.start()

    def stop(self):
        self._freeze.stop()
        self._gae_patch.stop()

    def __enter__(self):
        return self.start()

    def __exit__(self, *args):
        self.stop()


def freeze_time(time_to_freeze=None, tz_offset=0, ignore=None, tick=False):
    # Python3 doesn't have basestring, but it does have str.
    try:
        string_type = basestring
    except NameError:
        string_type = str

    if not isinstance(time_to_freeze, (string_type, datetime.date)):
        raise TypeError(('freeze_time() expected None, a string, date instance, or '
                         'datetime instance, but got type {0}.').format(type(time_to_freeze)))
    if tick and not _is_cpython:
        raise SystemError('Calling freeze_time with tick=True is only compatible with CPython')

    if ignore is None:
        ignore = []
    ignore.append('six.moves')
    ignore.append('django.utils.six.moves')
    return _freeze_time(time_to_freeze, tz_offset, ignore, tick)


class TestCase(HTTPStatusTestCaseMixin, APITestCase):

    def setUp(self):
        super(TestCase, self).setUp()

        self.testbed = testbed.Testbed()
        self.testbed.activate()
        path = os.path.normpath(os.path.join(os.path.dirname(__file__), '../../'))
        self.testbed.init_taskqueue_stub(root_path=path)
        self.testbed.init_memcache_stub()
        self.testbed.init_datastore_v3_stub()
        self.taskqueue_stub = self.testbed.get_stub(testbed.TASKQUEUE_SERVICE_NAME)

    def tearDown(self):
        super(TestCase, self).tearDown()

        self.testbed.deactivate()

    def validate(self, data, schema):
        v = Draft4Validator(schema)
        if not v.is_valid(data):
            for error in sorted(v.iter_errors(data), key=str):
                if error.context:
                    self.fail("\n".join('{} {}'.format(cerror.absolute_path, cerror.message) for cerror in error.context))
                else:
                    self.fail(error.message)

    def validate_retrieve(self, response, schema):
        self.validate(response.data, schema)

    def validate_list(self, response, schema):
        self.validate(response.data['results'][0], schema['items']['oneOf'][0])
        self.validate(response.data['results'], schema)

    def get(self, path, data=None, follow=False, secure=False, **extra):
        print '***' * 15
        print 'GET {}'.format(path)
        print 'Authenticated' if '_auth_user_id' in self.client.session else 'Not Authenticated'
        response = self.client.get(path=path, data=data, follow=follow, secure=secure, **extra)
        print 'Response status code: {}'.format(response.status_code)
        print 'Response body:'
        print json.dumps(response.data)
        return response

    def post(self, path, data=None, content_type=None, follow=False, secure=False, **extra):
        print '***' * 15
        print 'POST {}'.format(path)
        print 'Authenticated' if '_auth_user_id' in self.client.session else 'Not Authenticated'
        print 'Request body:'
        print json.dumps(data)
        response = self.client.post(path=path, data=data, content_type=content_type, follow=follow, secure=secure,
                                    **extra)
        print 'Response status code: {}'.format(response.status_code)
        print 'Response body:'
        print json.dumps(response.data)
        return response

    def patch(self, path, data=None, content_type=None, follow=False, secure=False, **extra):
        print '***' * 15
        print 'PATCH {}'.format(path)
        print 'Authenticated' if '_auth_user_id' in self.client.session else 'Not Authenticated'
        print 'Request body:'
        print json.dumps(data)
        response = self.client.patch(path=path, data=data, content_type=content_type, follow=follow, secure=secure,
                                     **extra)
        print 'Response status code: {}'.format(response.status_code)
        print 'Response body:'
        print json.dumps(response.data)
        return response

    def put(self, path, data=None, content_type=None, follow=False, secure=False, **extra):
        print '***' * 15
        print 'PUT {}'.format(path)
        print 'Authenticated' if '_auth_user_id' in self.client.session else 'Not Authenticated'
        print 'Request body:'
        print json.dumps(data)
        response = self.client.put(path=path, data=data, content_type=content_type, follow=follow, secure=secure,
                                   **extra)
        print 'Response status code: {}'.format(response.status_code)
        print 'Response body:'
        print json.dumps(response.data)
        return response

    def delete(self, path, data=None, content_type=None, follow=False, secure=False, **extra):
        print '***' * 15
        print 'DELETE {}'.format(path)
        print 'Authenticated' if '_auth_user_id' in self.client.session else 'Not Authenticated'
        print 'Request body:'
        print json.dumps(data)
        response = self.client.delete(path=path, data=data, content_type=content_type, follow=follow, secure=secure,
                                      **extra)
        print 'Response status code: {}'.format(response.status_code)
        print 'Response body:'
        print json.dumps(response.data)
        return response
