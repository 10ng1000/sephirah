from django.urls import path
from . import views

urlpatterns = [
    path('sse_invoke/', views.ChatSseView.as_view(), name='chat'),
    path('invoke/', views.ChatView.as_view(), name='chat'),
]