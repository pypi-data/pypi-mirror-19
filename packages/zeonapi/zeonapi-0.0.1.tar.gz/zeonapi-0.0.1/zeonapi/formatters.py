"""

Форматировщики данных

Created: 15.12.16 0:19
Author: Ivan Soshnikov, e-mail: ivan@wtp.su
"""

from abc import ABCMeta, abstractstaticmethod
import simplejson as json


class DocumentFormatterBase(metaclass=ABCMeta):
    """
    Базовый класс форматтеров документов
    """

    @abstractstaticmethod
    def save(document):
        raise NotImplemented('Method not implemented')


class DocumentFormatterJSON(DocumentFormatterBase):
    """
    Класс модель данных в JSON
    """

    @staticmethod
    def save(document):

        return json.dumps(document.get_dict(), sort_keys=True)


class DocumentFormatterCSV(DocumentFormatterBase):
    """
    Класс форматирует документ в CSV
    """

    @staticmethod
    def save(document, write_head=False):
        doc_data = document.get_dict()
        keys = list(doc_data.keys())
        keys.sort()
        result = ''
        if write_head:
            result = "%s\n" % ";".join([key for key in keys])

        result += "%s\n" % ";".join([str(doc_data.get(key)) for key in keys])

        return result
