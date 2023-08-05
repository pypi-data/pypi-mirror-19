
import json
import urlparse
from urllib import urlencode
from abc import ABCMeta, abstractmethod
from werkzeug.routing import BaseConverter, ValidationError
from querystring_parser import parser

class FormatException(Exception):
    pass

class FormatterFactory(object):

    _types = {}
    _instances = {}

    @staticmethod
    def register(name):
        def wrapper(cls):
            FormatterFactory._types[name] = cls
            return cls
        return wrapper

    @classmethod
    def exists(cls, name):
        return name in cls._types

    @classmethod
    def create(cls, name):
        if name not in cls._types:
            raise Exception()

        if name not in cls._instances:
            instance = cls._types[name]()
            instance.name = name
            cls._instances[name] = instance

        return cls._instances[name]

class FormatBase(object):

    __metaclass__ = ABCMeta
    name = None

    @abstractmethod
    def serialize(self, value):
        raise NotImplementedError()

    @abstractmethod
    def deserialize(self, value):
        raise NotImplementedError()

@FormatterFactory.register('json')
class JsonFormat(FormatBase):

    def serialize(self, value):
        try:
            return json.dumps(value)
        except ValueError as e:
            raise FormatException(e)

    def deserialize(self, value):
        try:
            return json.loads(value)
        except ValueError as e:
            raise FormatException(e)

@FormatterFactory.register('form-encoded')
class FormEncodedFormat(FormatBase):

    def serialize(self, value):
        if isinstance(value, list):
            raise NotImplementedError()
        return urlencode(value)

    def deserialize(self, value):
        return parser.parse(value, normalized = True)

class FormatConverter(BaseConverter):

    def to_python(self, value):
        if not FormatterFactory.exists(value):
            raise ValidationError()
        return FormatterFactory.create(value)
