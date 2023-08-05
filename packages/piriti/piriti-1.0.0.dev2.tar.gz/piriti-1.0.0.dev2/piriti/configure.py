
import logging
import logging.config

from config import config

logging.config.dictConfig(config['logger'])
 