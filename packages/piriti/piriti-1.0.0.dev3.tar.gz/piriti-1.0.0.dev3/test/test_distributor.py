
from piriti.message_distributor import MessageDistributor
from piriti.listener import Listener
from piriti.path import Path
from piriti.data_pack import DataPack

class FakeListener(Listener):

    def __init__(self):
        super(FakeListener, self).__init__(None, lambda x: x)
        self.messages = []

    def send(self, data):
        self.messages.append(data)

def test_dispatch_single_match():
    # Arrange
    distrib = MessageDistributor()
    listener = FakeListener()
    distrib.register(Path('/apple'), listener)
    data = {"the_answer": 42}

    # Act
    distrib.dispatch(DataPack(Path('/apple'), data))

    # Assert
    assert len(listener.messages) == 1
    assert listener.messages[0]['data'] == data

def test_dispatch_single_not_match():
    # Arrange
    distrib = MessageDistributor()
    listener = FakeListener()
    distrib.register(Path('/apple'), listener)
    data = {"the_answer": 42}

    # Act
    distrib.dispatch(DataPack(Path('/pear'), data))

    # Assert
    assert len(listener.messages) == 0

def test_dispatch_sub_tree_match():
    # Arrange
    distrib = MessageDistributor()
    listener = FakeListener()
    distrib.register(Path('/apple'), listener)
    data = {"the_answer": 42}

    # Act
    distrib.dispatch(DataPack(Path('/apple/core'), data))

    # Assert
    assert len(listener.messages) == 1
    assert listener.messages[0]['data'] == data

def test_dispatch_sub_tree_not_match():
    # Arrange
    distrib = MessageDistributor()
    listener = FakeListener()
    distrib.register(Path('/apple/core'), listener)
    data = {"the_answer": 42}

    # Act
    distrib.dispatch(DataPack(Path('/apple'), data))

    # Assert
    assert len(listener.messages) == 0

def test_register():
    # Arrange
    distrib = MessageDistributor()
    listener = FakeListener()
    path = Path('/apple/core')

    # Act
    distrib.register(path, listener)

    # Assert
    assert len(distrib._listeners) == 1
    assert distrib._listeners['/apple/core'] == [listener]


def test_unregister():
    # Arrange
    distrib = MessageDistributor()
    listener = FakeListener()
    path = Path('/apple/core')
    distrib.register(path, listener)
    assert len(distrib._listeners) == 1

    # Act
    res = distrib.unregister(listener)

    # Assert
    assert res
