from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

from django.urls import path
from lectures.consumers import LectureConsumer

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            [
                path('ws/lecture/<str:token>/', LectureConsumer),
            ]
        )
    ),
})
