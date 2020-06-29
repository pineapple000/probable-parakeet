import yaml
import logging
import logging.config
from logging_config import LOGGING
from connect import MongoConnection
from datetime import datetime

logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)


class CommentYAML:
    """Comment YAML operations"""

    def insert_yaml(self, yaml_comment):
        try:
            comment = yaml.safe_load(yaml_comment)

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
        except Exception as e:
            logger.error('Could not save the comment: %s' % e)
        finally:
            conn.client.close()

