from django.template.defaulttags import url
from django.urls import re_path

from app import consumers

websocket_urlpatterns = [
    re_path(r'^test$', consumers.FeatureConsumer.as_asgi()),
]