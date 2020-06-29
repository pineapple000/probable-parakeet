import logging
import logging.config
from config import MONGODB
from logging_config import LOGGING
from pymongo import MongoClient, errors

logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)


class MongoConnection(object):

    def __init__(self):
        try:
            self.client = MongoClient(
                host=MONGODB.get('HOST'),
                port=MONGODB.get('PORT'),
                username=MONGODB.get('USER', None),
                password=MONGODB.get('PASSWORD', None)
            )
            self.db = self.client[MONGODB.get('NAME')]
        except errors.ConnectionFailure as e:
            logger.error('Server not available: %s' % e)
            raise e
        except errors.PyMongoError as e:
            logger.error('Connection error: %s' % e)
            raise e

