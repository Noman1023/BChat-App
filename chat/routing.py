from django.urls import re_path
from django.urls.conf import path

from . import consumers

websocket_urlpatterns = [
    path('ws/chat/inbox/<str:username>/', consumers.ChatConsumer),
]