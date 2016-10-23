# coding=utf-8

import logging
import traceback

from pymongo import MongoClient
from pymongo.errors import (ConnectionFailure,
                            NetworkTimeout,
                            DuplicateKeyError)

from utils import log_utils

__author__ = "linghanzhao"
__created__ = "10/23/16"

"""
File Description
"""

logging.basicConfig()
logger = logging.getLogger(__name__)

MONGOCLIENT = None


def get_client():
    """
    This function is to get the Mongo client
    :return MONGOCLIENT: a Database instance from a MongoClient.
    :rtype MONGOCLIENT: pymongo.mongo_client.MongoClient
    """

    global MONGOCLIENT

    if MONGOCLIENT is not None:
        return MONGOCLIENT

    MONGOCLIENT = MongoClient(host="localhost")
    return MONGOCLIENT


def get_db(name="Aerial"):
    """This function returns the database for the current application.

    :param name: database name.
    :type name: str.
    :return db: database.
    :rtype db: pymongo.database.Database.

    """
    try:
        client = get_client()
        db = client.get_database(name)
    except Exception as e:
        log_utils.log_msg_error(logger=logger, key='MONGOAPI0001', msg=name, values={"Exception": e.message})
        return None
    return db


def get_collections(db=None):
    """This function returns all collections in database, need to add more if more collections coming.

    :param db: database.
    :type db: pymongo.database.Database.
    :return collections: all collections in database.
    :rtype collections: dict

    """

    if db is None:
        log_utils.log_msg_error(logger=logger, key='MONGOAPI0002', msg='Cannot get Database')
        return None

    # Collections name
    soybeans = db.soybeans
    weathers = db.candidate_files

    collections = {
        'soybeans': soybeans,
        'weathers': weathers,

    }
    return collections

#######################################
#######    Database Insertion    ######
#######################################

def insert_one_document(collection=None, document=None):
    """This function inserts one document into the collection.

    :param collection: collection name.
    :type collection: pymongo.collection.Collection.
    :param document: json document.
    :type document: dict.
    :return id: inserted document ObjectId or -1 if insertion failed.
    :rtype id: ObjectId or int.

    """
    if collection is None or document is None:
        log_utils.log_msg_error(logger=logger, key='M002', msg='No collection name to insert document',
                                values={'collection': collection, 'doc': document})
        return -1

    try:
        id = collection.insert_one(document).inserted_id
    except TypeError as te:
        log_utils.log_msg_error(logger=logger, key='M003', msg='Failed to insert one document',
                                values={'collection': collection, 'doc': document}, exception=te)
        id = -1

    except NetworkTimeout as nt:
        log_utils.log_msg_error(logger=logger, key='M004', msg='Failed to insert one document',
                                values={'collection': collection, 'doc': document}, exception=nt)
        id = -1

    except ConnectionFailure as cf:
        log_utils.log_msg_error(logger=logger, key='M005', msg='Failed to insert one document',
                                values={'collection': collection, 'doc': document}, exception=cf)
        id = -1

    except DuplicateKeyError as dke:
        log_utils.log_msg_error(logger=logger, key='M006', msg='Failed to insert one document',
                                values={'collection': collection, 'doc': document}, exception=dke)
        id = -1

    return id

#######################################
#######    Database Lookup    #########
#######################################

def get_one_document(collection=None, query=None):
    """This function retrieves one document by query.

    :param collection: collection name.
    :type collection: pymongo.collection.Collection.
    :param query: json format, Sample: ({"field_name":value}).
    :type query: dict.
    :return document: the json document from db by query.
    :rtype document: dict.

    """
    if collection is None:
        log_utils.log_msg_info(logger=logger, key='M013', msg='Missing collection name to get one document',
                               values={'collection': collection, 'doc': query}, exception="")
        return None
    if query is None:
        log_utils.log_msg_info(logger=logger, key='M014', msg='Missing query info to get one document',
                               values={'collection': collection, 'doc': query}, exception="")
        return None

    document = None
    try:
        document = collection.find_one(query)

    except TypeError as te:
        log_utils.log_msg_error(logger=logger, key='M015', msg='Failed to retrieve one document',
                                values={'collection': collection, 'doc': document}, exception=te)
        return None

    except NetworkTimeout as nt:
        log_utils.log_msg_error(logger=logger, key='M016', msg='Failed to retrieve one document',
                                values={'collection': collection, 'doc': document}, exception=nt)
        return None

    except ConnectionFailure as cf:
        log_utils.log_msg_error(logger=logger, key='M017', msg='Failed to retrieve one document',
                                values={'collection': collection, 'doc': document}, exception=cf)
        return None

    return document


def get_all_document(collection=None):
    """The function gets all documents in a certain collection.

    :param collection: collection name.
    :type collection: pymongo.collection.Collection.
    :return documents: all documents under this collection.
    :rtype documents: pymongo.command_cursor.CommandCursor.

    """
    if collection is None:
        log_utils.log_msg_error(logger=logger, key='M036', msg='Missing collection to retrieve all document',
                                values={'collection': collection}, exception="")
        return None

    documents = None

    try:
        documents = collection.find().batch_size(50)

    except TypeError as te:
        traceback.print_exc()
        log_utils.log_msg_error(logger=logger, key='M037', msg='Failed to Retrieve all documents',
                                values={'collection': collection}, exception=te)

    except NetworkTimeout as nt:
        traceback.print_exc()
        log_utils.log_msg_error(logger=logger, key='M038', msg='Failed to Retrieve document',
                                values={'collection': collection}, exception=nt)

    except ConnectionFailure as cf:
        traceback.print_exc()
        log_utils.log_msg_error(logger=logger, key='M039', msg='Failed to Retrieve all documents',
                                values={'collection': collection}, exception=cf)

    return documents
