
import os
from werkzeug.routing import PathConverter as PathConverterBase

from .exceptions import InvalidPath

class Path(object):

    def __init__(self, path = '/'):
        if not path or not path.startswith('/'):
            raise InvalidPath("Path '{}' is invalid!".format(path))
        self._path = path

    @property
    def path(self):
        return self._path

    def get_all_sub_path(self):
        yield '/'
        if self._path == '/':
            return
        path_parts = []                        
        for part in self.path.split("/"):
            path_parts.append(part)
            sub_path = "/".join(path_parts)
            if sub_path != '':
                yield sub_path

    def __repr__(self):
        return "<Path path = '{}'>".format(self.path)

class PathConverter(PathConverterBase):        
    def to_python(self, value):
        return Path('/' + os.path.normpath(value))
