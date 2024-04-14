from django.db import close_old_connections
from channels.middleware import BaseMiddleware
from rest_framework_simplejwt.tokens import UntypedToken
from .utils import LOGGER, get_user


class JwtAuthMiddleware(BaseMiddleware):
    """
    Custom middleware for JWT Authentication
    """

    def __init__(self, inner):
        super().__init__(inner)

    async def __call__(self, scope, receive, send):
        close_old_connections()

        token_from_querystring = self.get_token_from_querystring(scope)

        if not token_from_querystring:
            raise Exception("Invalid token type")

        try:
            untyped_token = UntypedToken(token_from_querystring).payload
            scope['user'] = await get_user(untyped_token.get('user_id'))
        except Exception as e:
            LOGGER.error(e)
            return None

        return await super().__call__(scope, receive, send)

    @staticmethod
    def get_token_from_querystring(scope):
        """
        Retrieve token from querystring

        :param dict scope: channel layer scope
        :return: str
        """
        query_string_dict = dict(k_v.split('=') for k_v in scope['query_string'].decode("utf-8").split("&"))

        return query_string_dict.get('token')


from channels.auth import AuthMiddlewareStack

def JWTAuthMiddlewareStack(inner):
    return JwtAuthMiddleware(AuthMiddlewareStack(inner))
