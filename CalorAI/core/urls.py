from django.urls import path
from .views import SendMessageToUsersView

urlpatterns = [
    path("send-message/", SendMessageToUsersView.as_view(), name="send-message"),
]
