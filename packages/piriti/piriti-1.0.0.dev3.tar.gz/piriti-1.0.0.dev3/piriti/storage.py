
from abc import ABCMeta, abstractmethod
from path import Path

from .data_pack import DataPack

class MessageStorageBase(object):

    __metaclass__ = ABCMeta

    @abstractmethod
    def store(self, data_pack):
        """Store the data pack in somewhat backend

        Args:
            data_pack (DataPack): data pack to store

        Returns:
            bool: the storing was successfull or not
        """
        raise NotImplementedError()

    @abstractmethod
    def fetch(self, path):
        """Fetch data by path string

        Args:
            path (str): path string

        Returns:
            list: list of DataPack instances ordered by time
        """
        raise NotImplementedError()

class MessageStorageMemory(MessageStorageBase):

    def __init__(self, initial_data = None):
        self._data = initial_data or {}

    def store(self, data_pack):
        path_str = data_pack.path.path
        if path_str not in self._data:
            self._data[path_str] = []
        self._data[path_str].append(data_pack)
        return True

    def fetch(self, path):
        res = []
        if len(path.path):
            for data_path, data_list in self._data.items():
                for sub_path in Path(data_path).get_all_sub_path():
                    if sub_path == path.path:
                        res += data_list
        else:
            for data_path, data_list in self._data.items():
                res += data_list
            return res

        return sorted(res, key = lambda dp: dp.time)
