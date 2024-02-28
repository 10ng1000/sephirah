from django.urls import path
from . import views

urlpatterns = [
    path('sse_invoke', views.ChatSseView.as_view(), name='chat'),
    path('invoke', views.ChatView.as_view(), name='invoke'),
    path('sessions', views.ChatSessionsView.as_view(), name='sessions'),
    path('sessions/<str:session_id>', views.ChatSessionView.as_view(), name='session'),
    path('sessions/<str:session_id>/books', views.ChatSessionBooksView.as_view(), name='session_books'),
]