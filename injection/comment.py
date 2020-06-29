import pymongo
import logging
import logging.config
from logging_config import LOGGING
from connect import MongoConnection
from datetime import datetime

logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)


class Comment:
    """Comment operations"""

    def insert(self, comment):
        try:
            conn = MongoConnection()

            discussion_id = comment.get('discussion_id')
            parent_slug = comment.get('parent_slug')
            slug = comment.get('slug')
            full_slug = comment.get('full_slug')

            if parent_slug:
                parent = conn.db.comments.find_one(
                    {'discussion_id': discussion_id, 'slug': parent_slug})
                slug = '%s/%s' % (parent['slug'], slug)
                full_slug = '%s/%s' % (parent['full_slug'], full_slug)

            conn.db.comments.insert({
                'discussion_id': discussion_id,
                'slug': slug,
                'full_slug': full_slug,
                'posted': datetime.utcnow(),
                'author': comment.get('author_info'),
                'text': comment.get('comment_text'),
                'is_private': comment.get('private', False)
            })
        except pymongo.errors.PyMongoError as e:
            logger.error('Could not save the comment: %s' % e)
        except Exception as e:
            logger.error('Could not save the comment: %s' % e)
        finally:
            conn.client.close()

    def find(self, discussion_id, page_num=0, page_size=20):
        results = []
        try:
            conn = MongoConnection()

            cursor = conn.db.comments.find(
                {'discussion_id': discussion_id},
                sort=[('posted', 1)],
                skip=page_num * page_size,
                limit=page_size
            )
            results = [comments for comments in cursor]
            cursor.close()
        except pymongo.errors.PyMongoError as e:
            logger.error('Could not find the comment: %s' % e)
        except Exception as e:
            logger.error('Could not find the comment: %s' % e)
        finally:
            conn.client.close()
        return results

    def find_text(self, query, page_num=0, page_size=20):
        results = []
        try:
            conn = MongoConnection()

            cursor = conn.db.comments.find(
                {
                    '$where': (
                        'this.is_private == false && '
                        'this.text  == "' + query + '"')
                },
                sort=[('posted', 1)],
                skip=page_num * page_size,
                limit=page_size
            )
            results = [comments for comments in cursor]
            cursor.close()
        except pymongo.errors.PyMongoError as e:
            logger.error('Could not find the comment: %s' % e)
        except Exception as e:
            logger.error('Could not find the comment: %s' % e)
        finally:
            conn.client.close()
        return results

    def update(self, slug, comment_text):
        try:
            conn = MongoConnection()

            conn.db.comments.update_one(
                {'slug': slug},
                {'$set': {'text': comment_text}}
            )
        except pymongo.errors.PyMongoError as e:
            logger.error('Could not update the comment: %s' % e)
        except Exception as e:
            logger.error('Could not update the comment: %s' % e)
        finally:
            conn.client.close()

    def delete(self, slug):
        try:
            conn = MongoConnection()

            conn.db.comments.delete_one(
                {'slug': slug, 'is_private': False})
        except pymongo.errors.PyMongoError as e:
            logger.error('Could not delete the comment: %s' % e)
        except Exception as e:
            logger.error('Could not delete the comment: %s' % e)
        finally:
            conn.client.close()

    def delete_many(self, slug):
        try:
            conn = MongoConnection()

            conn.db.comments.delete_many({
                'slug': {'$regex': slug, '$options': 'i'},
                'is_private': False
            })
        except pymongo.errors.PyMongoError as e:
            logger.error('Could not delete the comments: %s' % e)
        except Exception as e:
            logger.error('Could not delete the comments: %s' % e)
        finally:
            conn.client.close()

