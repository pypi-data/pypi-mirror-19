
import logging

logger = logging.getLogger(__name__)

class MessageDistributor(object):

    def __init__(self, initial = None):
        self._listeners = initial or {}

    def register(self, path, listener):
        if path not in self._listeners:
            self._listeners[path.path] = []
        self._listeners[path.path].append(listener)
        logger.info("Listener %s registered to '%s'", listener, path)

    def unregister(self, listener):
        cnt = 0
        for path in self._listeners:
            for removable_listener in [s for s in self._listeners[path] if s.id == listener.id]:
                self._listeners[path].remove(removable_listener)
                cnt += 1
                logger.info("Listener (%s: %s) unregistered", path, removable_listener)

        return bool(cnt)

    def dispatch(self, data_pack):
        """Dispatch

        Args:
            data_pack (DataPack): data_pack
        """
        listeners = []
        for sub_path in data_pack.path.get_all_sub_path():
            listeners += self._listeners.get(sub_path, [])

        logger.info("Dispatch data (%s) to %s listeners", data_pack.path, len(listeners))

        for listener in listeners:
            listener.send(data_pack.as_dict)
