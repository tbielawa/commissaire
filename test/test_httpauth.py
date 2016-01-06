# Copyright (C) 2016  Red Hat, Inc
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
Test cases for the commissaire.authentication.httpauth module.
"""

import falcon

from . import TestCase
from falcon.testing.helpers import create_environ
from commissaire.authentication import httpauth


class Test_HTTPBasicAuth(TestCase):
    """
    Tests for the _HTTPBasicAuth class.
    """

    def setUp(self):
        """
        Sets up a fresh instance of the class before each run.
        """
        self.http_basic_auth = httpauth._HTTPBasicAuth()

    def test_decode_basic_auth_with_header(self):
        """
        Verify decoding returns a filled tuple given the proper header no matter the case of basic.
        """
        basic = list('basic')
        for x in range(0, 5):
            headers = {'Authorization': '{0} YTph'.format(''.join(basic))}
            req = falcon.Request(
                create_environ(headers=headers))
            self.assertEquals(
                ('a', 'a'),
                self.http_basic_auth._decode_basic_auth(req))
            # Update the next letter to be capitalized
            basic[x] = basic[x].capitalize()

    def test_decode_basic_auth_with_bad_data_in_header(self):
        """
        Verify decoding returns no user with bad base64 data in the header.
        """
        req = falcon.Request(
            create_environ(headers={'Authorization': 'basic BADDATA'}))
        self.assertEquals(
            (None, None),
            self.http_basic_auth._decode_basic_auth(req))

    def test_decode_basic_auth_with_no_header(self):
        """
        Verify returns no user with no authorization header.
        """
        req = falcon.Request(create_environ(headers={}))
        self.assertEquals(
            (None, None),
            self.http_basic_auth._decode_basic_auth(req))


class TestHTTPBasicAuthByFile(TestCase):
    """
    Tests for the HTTPBasicAuthByFile class.
    """

    def setUp(self):
        """
        Sets up a fresh instance of the class before each run.
        """
        self.http_basic_auth_by_file = httpauth.HTTPBasicAuthByFile(
            './conf/users.yaml')

    def test_load_with_non_parsable_file(self):
        """
        Verify load gracefully loads no users when the YAML file does not exist.
        """
        for bad_file in ('', 'test/bad.yaml'):
            self.http_basic_auth_by_file.filepath = bad_file
            self.http_basic_auth_by_file.load()
            self.assertEquals(
                {},
                self.http_basic_auth_by_file._data
            )

    def test_autenticate_with_valid_user(self):
        """
        Verify authenticate works with a proper YAML file, Authorization header, and a matching user.
        """
        self.http_basic_auth_by_file = httpauth.HTTPBasicAuthByFile(
            './conf/users.yaml')
        req = falcon.Request(
            create_environ(headers={'Authorization': 'basic YTph'}))
        resp = falcon.Response()
        self.assertEquals(
            None,
            self.http_basic_auth_by_file.authenticate(req, resp))

    def test_autenticate_with_invalid_user(self):
        """
        Verify authenticate denies with a proper YAML file, Authorization header, and no matching user.
        """
        self.http_basic_auth_by_file = httpauth.HTTPBasicAuthByFile('./conf/users.yaml')
        req = falcon.Request(
            create_environ(headers={'Authorization': 'basic Yjpi'}))
        resp = falcon.Response()
        self.assertRaises(
            falcon.HTTPForbidden,
            self.http_basic_auth_by_file.authenticate,
            req, resp)
