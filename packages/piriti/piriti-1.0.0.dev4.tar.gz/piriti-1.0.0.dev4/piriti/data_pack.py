
from datetime import datetime

class DataPack(object):
    def __init__(self, path, data, time = None):
        self._path = path
        self._data = data
        self._time = time or datetime.now()

    @property
    def path(self):
        return self._path

    @property
    def data(self):
        return self._data

    @property
    def time(self):
        return self._time

    @property
    def as_dict(self):  
        return {
            "time": self._time.isoformat(),
            "path": self._path.path,
            "data": self._data,
        }
