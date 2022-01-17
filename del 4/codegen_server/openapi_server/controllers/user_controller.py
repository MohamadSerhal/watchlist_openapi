import connexion
import six

from openapi_server.models.inline_response200 import InlineResponse200  # noqa: E501
from openapi_server.models.show_rating import ShowRating  # noqa: E501
from openapi_server.models.user_auth_body import UserAuthBody  # noqa: E501
from openapi_server.models.user_register_body import UserRegisterBody  # noqa: E501
from openapi_server.models.user import User
from openapi_server import util

from .auth_module import authentication_module
from passlib.hash import sha256_crypt
from .mongo.mongo_connection import db
import pymongo
from flask import make_response, jsonify
import json
from bson import json_util
from bson.objectid import ObjectId

users_collection = db.users
shows_collection = db.shows

def add_to_watchlist(show_id, user):  # noqa: E501
    """add_to_watchlist

    Adds show to the user&#39;s watchlist # noqa: E501

    :param show_id: 
    :type show_id: str

    :rtype: None
    """
    u = users_collection.find_one({"_id": ObjectId(user), "watchlist": show_id})
    if u is not None:
        return make_response("Cant add show to watchlist! It already exists there.", 400)
    users_collection.update_one({"_id": ObjectId(user)}, {'$push': {'watchlist': show_id}})
    return make_response("Added show to watchlist", 201)

def delete_from_watchlist(show_id, user):  # noqa: E501
    """delete_from_watchlist

    Delete show from user&#39;s watchlist # noqa: E501

    :param show_id: 
    :type show_id: str

    :rtype: InlineResponse200
    """
    users_collection.update_one({"_id": ObjectId(user)}, {'$pull': {'watchlist': show_id}})
    return make_response("Removed show from watchlist", 200) 


def get_watchlist(user):  # noqa: E501
    """get_watchlist

    Gets the user&#39;s watchlist # noqa: E501


    :rtype: List[str]
    """
    user_found = users_collection.find_one({"_id": ObjectId(user)})
    if user_found is None:
        return make_response("No user with such id exists", 403)
    return make_response( jsonify( json.loads(json_util.dumps(user_found["watchlist"])) ), 200)


def login_user():  # noqa: E501
    """login_user

    login user and returns a json web token # noqa: E501

    :param user_auth_body: 
    :type user_auth_body: dict | bytes

    :rtype: InlineResponse200
    """
    if connexion.request.is_json:
        user_auth_body = UserAuthBody.from_dict(connexion.request.get_json())  # noqa: E501
        user_found = users_collection.find_one({"username": user_auth_body._username})
        if user_found is None:
            return make_response("User with this username does not exist!", 403)
        authenticated = sha256_crypt.verify(user_auth_body._password, user_found["hashed_pass"])
        if authenticated == False:
            return make_response("Invalid username or password!", 403)
        u = json.loads(json_util.dumps(user_found))
        token = authentication_module.create_token(u['_id']['$oid'])
        return make_response(token, 200)
    return make_response("ERROR: Request body should be JSON", 400)



def rate_show():  # noqa: E501
    """rate_show

    User rates a show, this also affects the show&#39;s total rating # noqa: E501

    :param show_rating: 
    :type show_rating: dict | bytes

    :rtype: InlineResponse200
    """
    if connexion.request.is_json:
        show_rating = ShowRating.from_dict(connexion.request.get_json())  # noqa: E501
        if show_rating._rating > 5 or show_rating._rating < 0:
            return make_response("Show rating must be an integer between 0 or 5 inclusive.", 400)
        s = shows_collection.find_one({"_id": ObjectId(show_rating._show_id)})
        if s is None:
            return make_response("Show with this id doesnt exist", 400)
        ratings = s["rating_number"]
        newRating = (s["rating"] * ratings + show_rating._rating) / (ratings + 1)
        shows_collection.update_one({"_id": ObjectId(show_rating._show_id)}, {"$set": {"rating": newRating, "rating_number": s["rating_number"] + 1}})
        return make_response("Show rated", 200)
    return make_response("Body should be Json", 400)


def register_user():  # noqa: E501
    """register_user

    register user to the app # noqa: E501

    :param user_register_body: 
    :type user_register_body: dict | bytes

    :rtype: InlineResponse200
    """
    if connexion.request.is_json:
        user_register_body = UserRegisterBody.from_dict(connexion.request.get_json())  # noqa: E501
        hashed = sha256_crypt.encrypt(user_register_body._password)
        json_user = {"username":user_register_body._username,
                        "full_name": user_register_body._full_name,
                        "hashed_pass": hashed, 
                        "watchlist": []}
        users_collection.create_index([ ("username", pymongo.ASCENDING) ] , unique= True)
        u_json = json.dumps(json_user)
        data = json.loads(u_json)
        try: 
            users_collection.insert_one(data)
            return make_response("Created user successfully", 200)
        except:
            return make_response("ERROR: Cant add show, username must be unique!", 500)
    return make_response("ERROR: Request body should be JSON", 400)