from core.db.Singleton import Singleton
from pymongo import MongoClient
import urllib
from urllib.parse import quote


class MongoDB(metaclass=Singleton):

    def __init__(self, mongo_uri=None):
        self.__mongo_uri = mongo_uri

    def get_database(self):
        mongo_client = MongoClient("mongodb://" + self.__mongo_uri['user'] +
                                   ":" + urllib.parse.quote(self.__mongo_uri['password']) +
                                   "@" + self.__mongo_uri['host'] + ":" + self.__mongo_uri['port'] +
                                   "/" + self.__mongo_uri['db'])
        return mongo_client[self.__mongo_uri['db']]

    def __set__(self, instance, value):
        self.__mongo_uri(instance, value)
