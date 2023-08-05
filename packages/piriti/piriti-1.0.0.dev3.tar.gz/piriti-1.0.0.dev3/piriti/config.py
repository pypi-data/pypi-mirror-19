
import yaml
import os
from voidpp_tools.config_loader import ConfigLoader, ConfigFormatter, ConfigFileNotFoundException

class YamlConfigFormatter(ConfigFormatter):

    def encode(self, data):
        return yaml.safe_dump(data)

    def decode(self, data):
        return yaml.load(data)

loader = ConfigLoader(YamlConfigFormatter(), __file__)

try:
    config = loader.load('piriti.yaml')
except ConfigFileNotFoundException as e:
    print(e)
    print("See the example: https://github.com/voidpp/piriti/config_example.yaml")
    config = None
