
import logging

logger = logging.getLogger(__name__)

class Listener(object):
    __id = 0

    @classmethod
    def _get_next_id(cls):
        cls.__id += 1
        return cls.__id

    def __init__(self, websocket, serializer):
        self._websocket = websocket
        self._serializer = serializer
        self._id = self._get_next_id()
        logger.debug("Listener created with id %s", self.id)

    @property
    def id(self):
        return self._id

    def send(self, data):
        self._websocket.send(self._serializer(data))

    def __str__(self):
        return "<Listener id: {}, socket: {}>".format(self._id, self._websocket)
