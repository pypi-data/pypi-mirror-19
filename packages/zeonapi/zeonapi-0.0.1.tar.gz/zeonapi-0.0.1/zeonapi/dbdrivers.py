"""

Драйверы хранилищ данных

Created: 15.12.16 0:23
Author: Ivan Soshnikov, e-mail: ivan@wtp.su
"""

from abc import ABCMeta, abstractmethod
from pymongo import MongoClient


class DbDriverBase(metaclass=ABCMeta):
    """
    Базовый класс драйвера базы данных.
    Или любого другого хранилища данных.
    """

    @abstractmethod
    def save(self, document):
        raise NotImplemented('Method not implemented')

    @abstractmethod
    def exists(self, message_id):
        """
        Проверить, есть ли сообщение в БД
        :param message_id: идентификатор сообщения по заголовку Message-ID
        :return:
        """
        raise NotImplemented('Method not implemented')


class DbDriverMongo(DbDriverBase):
    """
    Драйвер БД для монги
    """

    def __init__(self, db_uri, db_name, db_collection):
        """

        :param db_uri: Строка подключения к БД
        :param db_name: Имя БД
        :param db_collection: Имя коллекции для сохранения данных о звонках
        """
        super(DbDriverMongo, self).__init__()
        # инициализация монги
        self._client = MongoClient(db_uri)
        self._db = self._client[db_name]
        self._collection = self._db[db_collection]

    def save(self, document):
        return self._collection.insert_one(document).inserted_id

    def exists(self, message_id):

        return self._collection.find({'id': message_id}).count() > 0
