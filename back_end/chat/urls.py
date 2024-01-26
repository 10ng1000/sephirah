from django.urls import path
from . import views

urlpatterns = [
    path('sse_invoke', views.ChatSseView.as_view(), name='chat'),
    path('invoke', views.ChatView.as_view(), name='invoke'),
    path('sessions', views.ChatSessionView.as_view(), name='sessions'),
    path('sessions/<str:session_id>', views.ChatSessionView.as_view(), name='session'),
]