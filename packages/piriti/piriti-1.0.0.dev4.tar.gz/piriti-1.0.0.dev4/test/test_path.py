
import pytest

from piriti.path import Path
from piriti.exceptions import InvalidPath

@pytest.mark.parametrize("name,input,expected", [
    ('simple', '/node1/node2/node3', ['/', '/node1', '/node1/node2', '/node1/node2/node3']),
    ('root', '/', ['/']),
])
def test_sub_path(name, input, expected):
    # Arrange
    path = Path(input)

    # Act
    sub_path = list(path.get_all_sub_path())

    # Assert
    assert sub_path == expected

@pytest.mark.parametrize("name,input", [
    ('empty', ''),
    ('None', None),
])
def test_sub_path_error(name, input):
    # Arrange & Act & Assert
    with pytest.raises(InvalidPath):
        Path('')
