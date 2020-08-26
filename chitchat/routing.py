from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter, ChannelNameRouter
import chat.routing
from chat import consumers
# from chat.auth_token_middleware import jwt_token_auth_middleware_stack
# from chat.auth_token_middleware import JwtTokenAuthMiddleware

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),
    # "channel": ChannelNameRouter({
    #         "asdf": consumers.NotificationConsumer,
    #     })
    # 'channel': ChannelNameRouter({
    #         'task': consumers.TaskConsumer
    #     })
})