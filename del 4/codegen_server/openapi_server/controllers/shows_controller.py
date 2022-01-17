import connexion
import six

from openapi_server.models.inline_response200 import InlineResponse200  # noqa: E501
from openapi_server.models.inline_response400 import InlineResponse400  # noqa: E501
from openapi_server.models.shows import Shows  # noqa: E501
from openapi_server import util

from .mongo.mongo_connection import db
from flask import  make_response, jsonify
from bson import json_util
from bson.objectid import ObjectId
import json
import pymongo

shows_collection = db.shows

def add_show():  # noqa: E501
    """add_show

    Add show to DB # noqa: E501

    :param shows: 
    :type shows: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        shows = connexion.request.get_json()  # noqa: E501
        shows_collection.create_index([ ("name", pymongo.ASCENDING) ] , unique= True)
        try: 
            result = shows_collection.insert_one(shows)
            return make_response("Added show successfully", 201)
        except:
            return make_response("ERROR: Cant add show, name must be unique!", 500)
    return make_response("ERROR: Request body should be JSON", 400)


def delete_show(show_id):  # noqa: E501
    """delete_show

    Deletes a show from the DB # noqa: E501

    :param show_id: 
    :type show_id: str

    :rtype: InlineResponse200
    """
    shows_collection.delete_one( {"_id": ObjectId(show_id)} )
    return make_response("Successfully deleted show from DB!", 200)


def get_show(show_id):  # noqa: E501
    """get_show

    Returns a show from the DB if it exists # noqa: E501

    :param show_id: 
    :type show_id: str

    :rtype: Shows
    """
    show_found = shows_collection.find_one({"_id": ObjectId(show_id)})
    if show_found is None:
        return make_response("Show does not exist in DB!", 404)
    return make_response( json.loads(json_util.dumps(show_found)), 200)


def get_shows_list(limit=None, offset=None):  # noqa: E501
    """get_shows_list

    Gets a show # noqa: E501

    :param limit: Limits the number of items on a page
    :type limit: int
    :param offset: Specifies the page number of the items to be displayed
    :type offset: int

    :rtype: List[Shows]
    """
    if limit < 0 or offset < 0:
        return make_response("Offset and limit have to be non negative integers", 400)
    shows_found = shows_collection.find().sort("name", pymongo.ASCENDING).skip(offset * limit).limit(limit)
    return make_response(jsonify( json.loads(json_util.dumps(shows_found)) ) , 200)