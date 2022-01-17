# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from openapi_server.models.inline_response200 import InlineResponse200  # noqa: E501
from openapi_server.models.show_rating import ShowRating  # noqa: E501
from openapi_server.models.user_auth_body import UserAuthBody  # noqa: E501
from openapi_server.models.user_register_body import UserRegisterBody  # noqa: E501
from openapi_server.test import BaseTestCase


class TestUserController(BaseTestCase):
    """UserController integration test stubs"""

    def test_add_to_watchlist(self):
        """Test case for add_to_watchlist

        
        """
        headers = { 
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/user/watchlist/{show_id}'.format(show_id='show_id_example'),
            method='PATCH',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_from_watchlist(self):
        """Test case for delete_from_watchlist

        
        """
        headers = { 
            'Accept': 'application/json',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/user/watchlist/{show_id}'.format(show_id='show_id_example'),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_watchlist(self):
        """Test case for get_watchlist

        
        """
        headers = { 
            'Accept': 'application/json',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/user/watchlist',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_login_user(self):
        """Test case for login_user

        
        """
        user_auth_body = openapi_server.UserAuthBody()
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/user/login',
            method='POST',
            headers=headers,
            data=json.dumps(user_auth_body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_rate_show(self):
        """Test case for rate_show

        
        """
        show_rating = openapi_server.ShowRating()
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/user/rate',
            method='POST',
            headers=headers,
            data=json.dumps(show_rating),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_register_user(self):
        """Test case for register_user

        
        """
        user_register_body = openapi_server.UserRegisterBody()
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/user/register',
            method='POST',
            headers=headers,
            data=json.dumps(user_register_body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
