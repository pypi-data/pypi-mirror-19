"""

Класс, предназначенный для получения и разбора почтовых
уведомлений с записью разговоров

Created: 14.12.16 12:05
Author: Ivan Soshnikov, e-mail: ivan@wtp.su
"""

import base64
import contextlib
import datetime
import email
import hashlib
import os
import wave
import tempfile
from abc import ABCMeta, abstractmethod
from imaplib import IMAP4, IMAP4_SSL
from poplib import POP3, POP3_SSL
import pydub
import progressbar

from bs4 import BeautifulSoup
from dateutil.parser import *  # http://dateutil.readthedocs.io/en/stable/index.html#

# типы получаемых сообщений: только новые, все подряд
MSG_NEW = 'NEW'
MSG_ALL = 'ALL'


def normalize_phone(phone):
    """
    Привести номер телефона к стандартному цифровому виду
    :param phone:
    :return:
    """

    digit_phone = "".join([r for r in phone if r.isdigit()])
    if len(digit_phone) == 11 and (digit_phone[0] == '7' or digit_phone[0] == '8'):
        digit_phone = digit_phone[1:]

    return digit_phone


class RecordModel:
    """
    Модель данных информации о звонке
    """

    def __init__(self):
        self.message_datetime = None
        self.message_id = None
        self.message_record_datetime = None
        self.message_direction = None
        self.message_caller_a = None
        self.message_caller_b = None
        self.message_wav_hash = None
        self.message_duration = None

    def get_dict(self):
        prefix = 'message_'

        keys = [key[len(prefix):] for key in self.__dict__.keys() if key.startswith(prefix)]
        result = {}
        for key in keys:
            result[key] = self.__dict__.get("%s%s" % (prefix, key))

        return result


class MainMessageProcessor:
    """
    Обработать часть сообщения, содержащее текстовое описание звонка
    """

    @classmethod
    def parse_message(cls, message):
        content_type = message.get('Content-Type')
        if content_type is None:
            return None
        if not content_type.startswith('multipart/related;'):
            return None

        result = cls()
        result.type = 'MAIN_MESSAGE'

        for msg in message.get_payload():
            if msg.get('Content-Type').startswith('text/html'):
                result.src_msg = msg.get_payload()

                fld_convert = {
                    'Время': 'record_datetime',
                    'Тип звонка': 'direction',
                    'Абонент А': 'caller_a',
                    'Абонент Б': 'caller_b',
                }

                call_types = {
                    'Локальный': 'local',
                    'Входящий': 'incoming',
                    'Исходящий': 'outgoing',
                }  # Есть еще трансфер, но на практике ни разу такого типа звонка не было ни разу

                soup = BeautifulSoup(result.src_msg, 'html.parser')
                table = soup.find('table', {'class': 'sidebarContent'}).find_all('tr')
                for row in table:
                    kv = row.find_all('td')
                    key = kv[0].text
                    val = kv[1].text
                    if key not in fld_convert.keys():
                        continue
                    if key == 'Время':
                        result.record_datetime = parse(val)
                    elif key == 'Тип звонка':
                        result.direction = call_types.get(val, 'UNKNOWN')
                    elif key.startswith('Абонент'):
                        result.__setattr__(fld_convert[key], normalize_phone(val))
                    else:
                        result.__setattr__(fld_convert[key], val)

        return result


class RecordMessageProcessor:
    """
    Обработать часть сообщения, содержащее вложенный аудиофайл
    """

    out_folder = None
    bitrate = '56k'
    tmp_folder = tempfile.TemporaryDirectory().name

    @classmethod
    def parse_message(cls, message):

        if cls.out_folder is None:
            raise ValueError("Не указан каталог для сохранения записей")

        if not os.path.isdir(cls.tmp_folder):
            os.makedirs(cls.tmp_folder)

        tmp_file = os.path.join(cls.tmp_folder, 'record.wav')
        content_type = message.get('Content-Type')
        if content_type is None:
            return None
        if not content_type.startswith('audio/x-wav;'):
            return None

        result = cls()
        result.type = 'RECORD_MESSAGE'
        result.src_msg = message

        raw_decoded_record = base64.b64decode(message.get_payload())
        result.src_wav_md5 = hashlib.md5(raw_decoded_record).hexdigest()
        out_filename = "%s.mp3" % result.src_wav_md5
        out_file = os.path.join(cls.out_folder, out_filename)
        fd = open(tmp_file, 'wb')
        fd.write(raw_decoded_record)
        fd.close()
        pydub.AudioSegment.from_wav(tmp_file).export(out_file, format='mp3', bitrate=cls.bitrate)

        with contextlib.closing(wave.open(tmp_file, 'r')) as f:
            frames = f.getnframes()
            rate = f.getframerate()
            duration = frames / float(rate)

        result.out_filename = out_filename
        result.duration = duration
        return result


class RecordMessage:
    """
    Класс предоставляет данные разобранного сообщения
    """

    def __init__(self, message):
        """
        :param message: электронное письмо (https://docs.python.org/3/library/email-examples.html)
        """

        if type(message) is not email.message.Message:
            raise ValueError("Неправильный тип собщения")

        # TODO: дать возможность добавлять внешние процессоры сообщений
        self._msg_processors = [MainMessageProcessor, RecordMessageProcessor]
        self.parts = []
        self.message = message
        self.date = ''
        self.message_id = ''

    def process_message(self):
        """
        Обработать сообщение
        :return:
        """
        date_tuple = email.utils.parsedate_tz(self.message.get('Date'))
        if date_tuple:
            self.date = datetime.datetime.fromtimestamp(email.utils.mktime_tz(date_tuple))
        self.message_id = self.message.get('Message-ID')[1:-1]

        # здесь разбираем сообщение по частям
        for part in self.message.get_payload():
            content_type = part.get('Content-Type')
            if content_type is None:
                pass

            for processor in self._msg_processors:
                res = processor.parse_message(part)
                if res is not None:
                    self.parts.append(res)


class MailParserBase(metaclass=ABCMeta):
    """
    Базовый класс парсера сообщений
    """

    def __init__(self, mail_server, mail_user, mail_password, mail_ssl=True):
        """
        :param mail_server: адрес IMAP4/POP3-сервера
        :param mail_user: имя пользователя
        :param mail_password: пароль
        :param mail_ssl: использовать SSL (по умолчанию) или нет
        """

        self.db_driver = None
        self.messages = []
        self.mail_server = mail_server
        self.mail_user = mail_user
        self.mail_password = mail_password
        self.mail_ssl = mail_ssl

    def set_out_folder(self, foldername):
        """
        Установить каталог для сохранения аудиозаписей
        :param foldername: имя каталога
        :return:
        """

        RecordMessageProcessor.out_folder = foldername

    @abstractmethod
    def get_messages(self, msg_count=-1, imap_folder='', msg_to_get=MSG_NEW):
        """
        :param msg_count: количество сообщений к получению. -1 - все доступные
        :param imap_folder: каталог на сервере в котором хранятся сообщения
        :param msg_to_get: какие сообщения забирать
        :return:
        """
        raise NotImplemented('Method not implemented')

    def process_message_record(self, msg):
        record_message = RecordMessage(msg)
        record_message.process_message()
        self.messages.append(record_message)
        if self.db_driver is not None:
            # сохранить данные в БД
            main_data = None
            record_data = None
            for part in record_message.parts:
                if part.type == 'RECORD_MESSAGE':
                    record_data = part
                if part.type == 'MAIN_MESSAGE':
                    main_data = part
            model = RecordModel()
            model.message_datetime = record_message.date
            model.message_id = record_message.message_id
            model.message_record_datetime = main_data.record_datetime
            model.message_direction = main_data.direction
            model.message_caller_a = main_data.caller_a
            model.message_caller_b = main_data.caller_b
            model.message_wav_hash = record_data.src_wav_md5
            model.message_duration = record_data.duration

            self.db_driver.save(model.get_dict())

    def email_loaded(self, message_id):
        """
        Проверить, загружено ли уже сообщение.
        :param message_id: поле заголовка Message-ID
        :return:
        """

        if self.db_driver is None:
            # если нет драйвера БД, проверять нечего, значит считаем сообщение не загруженным.
            return False

        return self.db_driver.exists(message_id)


class MailParserIMAP(MailParserBase):

    def __init__(self, mail_server, mail_user, mail_password, mail_ssl=False):
        super(MailParserIMAP, self).__init__(mail_server, mail_user, mail_password, mail_ssl)

    def get_messages(self, msg_count=-1, imap_folder='', msg_to_get=MSG_NEW):
        """
        Получить сообщения с сервера
        :param msg_count: количество сообщений к получению. -1 - все доступные
        :param imap_folder: каталог на сервере в котором хранятся сообщения
        :param msg_to_get: какие сообщения забирать
        :return:
        """

        if self.mail_ssl:
            server = IMAP4_SSL(self.mail_server)
        else:
            server = IMAP4(self.mail_server)

        server.login(self.mail_user, self.mail_password)

        rv, data = server.select(imap_folder, readonly=True)
        if rv == 'OK':
            st, data = server.search(None, msg_to_get)
            if st == 'OK':
                for num in data[0].decode('utf-8').split():
                    rv, data = server.fetch(num, '(RFC822)')
                    if rv != 'OK':
                        print("ERROR getting message %i" % num)
                    msg = email.message_from_string(data[0][1].decode('utf-8'))

                    self.process_message_record(msg)

                    if msg_count > 0:
                        msg_count -= 1
                    if msg_count == 0:
                        break

            server.close()
        server.logout()


class MailParserPOP(MailParserBase):
    """
    Получаем почту по POP3-протоколу
    """

    def __init__(self, mail_server, mail_user, mail_password, mail_ssl=False):
        """
        :param mail_server: адрес IMAP-сервеpassра
        :param mail_user: имя пользователя
        :param mail_password: пароль
        :param mail_ssl: использовать POP3 (по умолчанию) или POP3_SSL
        """

        super(MailParserPOP, self).__init__(mail_server, mail_user, mail_password, mail_ssl)
        self.mail_port = None

    def get_messages(self, msg_count=-1, imap_folder='', msg_to_get=MSG_NEW):

        if self.mail_ssl:
            self.mail_port = 995 if self.mail_port is None else self.mail_port
            mailbox = POP3_SSL(self.mail_server, self.mail_port)
        else:
            self.mail_port = 110 if self.mail_port is None else self.mail_port
            mailbox = POP3(self.mail_server, self.mail_port)
        mailbox.user(self.mail_user)
        mailbox.pass_(self.mail_password)
        (nums, _) = mailbox.stat()

        bar = progressbar.ProgressBar()

        for msg_num in bar(range(1, nums)):
            try:
                msg_headers_b = mailbox.top(msg_num, 0)
            except Exception:
                raise Exception('Message %i not found' % msg_num)

            msg = email.message_from_string("\n".join([l.decode('utf-8') for l in msg_headers_b[1]]))
            msg_id = msg.get('Message-ID')[1:-1]
            if self.email_loaded(msg_id):
                continue

            msg_b = mailbox.retr(msg_num)
            msg = email.message_from_string("\n".join([l.decode('utf-8') for l in msg_b[1]]))
            self.process_message_record(msg)
            print("%i - %s " % (msg_num, msg_id))

            if msg_count > 0:
                msg_count -= 1
            if msg_count == 0:
                break

        mailbox.close()
