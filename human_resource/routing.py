from django.urls import path
from .consumers import ChatConsumer

websocket_urlpatterns = [
    path("ws/messages/<int:pk>/", ChatConsumer.as_asgi()),
]