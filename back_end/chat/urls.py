from django.urls import path
from . import views

urlpatterns = [
    path('sse_invoke', views.ChatSseView.as_view(), name='chat'),
    path('invoke', views.ChatView.as_view(), name='invoke'),
    path('sse_invoke/web_search', views.ChatWebSearchView.as_view(), name='chat'),
    path('sse_invoke/rag', views.ChatRetrievalView.as_view(), name='retrieval_invoke'),
    path('sessions', views.ChatSessionsView.as_view(), name='sessions'),
    path('sessions/<str:session_id>', views.ChatSessionView.as_view(), name='session'),
    path('sessions/<str:session_id>/books', views.ChatSessionBooksView.as_view(), name='session_books'),
    path('sessions/<str:session_id>/books/<str:book_id>', views.ChatSessionBooksView.as_view(), name='session_book')
]