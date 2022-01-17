# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from openapi_server.models.inline_response200 import InlineResponse200  # noqa: E501
from openapi_server.models.inline_response400 import InlineResponse400  # noqa: E501
from openapi_server.models.shows import Shows  # noqa: E501
from openapi_server.test import BaseTestCase


class TestShowsController(BaseTestCase):
    """ShowsController integration test stubs"""

    def test_add_show(self):
        """Test case for add_show

        
        """
        shows = {
  "episodes_num" : 1,
  "name" : "name",
  "genre" : "genre",
  "rating" : 0.8008281904610115,
  "rating_number" : 6,
  "type" : "type"
}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/shows',
            method='POST',
            headers=headers,
            data=json.dumps(shows),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_show(self):
        """Test case for delete_show

        
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/show/{show_id}'.format(show_id='show_id_example'),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_show(self):
        """Test case for get_show

        
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/show/{show_id}'.format(show_id='show_id_example'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_shows_list(self):
        """Test case for get_shows_list

        
        """
        query_string = [('limit', 56),
                        ('offset', 56)]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/shows',
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
