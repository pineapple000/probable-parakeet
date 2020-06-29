import pymongo
import logging
from lxml import etree
from logging_config import LOGGING
from connect import MongoConnection
from datetime import datetime

logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)


class CommentXML:
    """Comment XML operations"""

    def insert(self, xml_comment):

        parser = etree.XMLParser(
            # replace entities by their text value
            resolve_entities=True,
            # prevent network access when looking up external documents
            no_network=False
        )
        try:
            tree = etree.parse(xml_comment, parser=parser)
        except (etree.ParseError, ValueError) as e:
            logger.error('XML parse error - %s' % e)
            raise e
        comment = tree.getroot()

        try:
            conn = MongoConnection()

            discussion_id = int(comment.find('discussion_id').text)
            parent_slug = comment.find('parent_slug')
            slug = comment.find('slug').text
            full_slug = comment.find('full_slug').text

            if parent_slug:
                parent = conn.db.comments.find_one(
                    {'discussion_id': discussion_id, 'slug': parent_slug.text})
                slug = '%s/%s' % (parent['slug'], slug)
                full_slug = '%s/%s' % (parent['full_slug'], full_slug)

            is_private = False
            if comment.find('private') is not None:
                is_private = bool(comment.find('private').text)

            conn.db.comments.insert({
                'discussion_id': discussion_id,
                'slug': slug,
                'full_slug': full_slug,
                'posted': datetime.utcnow(),
                'author': comment.find('author_info').text,
                'text': comment.find('comment_text').text,
                'is_private': is_private
            })
        except pymongo.errors.PyMongoError as e:
            logger.error('Could not save the comment: %s' % e)
        finally:
            conn.client.close()

