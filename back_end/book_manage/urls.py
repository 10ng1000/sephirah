from django.urls import path
from . import views

urlpatterns = [
    path('', views.BooksView.as_view()),
    path('<str:id>', views.SingleBookView.as_view()),
    path('<str:id>/chat-sessions', views.BookSessionView.as_view()),
]