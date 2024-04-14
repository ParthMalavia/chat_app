
import logging
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async


formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

User = get_user_model()

@database_sync_to_async
def get_user(user_id):
    try:
        return User.objects.get(pk=user_id)
    except:
        return AnonymousUser()


def get_logger():
    logger = logging.getLogger(__name__)
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger

LOGGER = get_logger()
