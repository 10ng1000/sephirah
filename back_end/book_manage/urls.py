from django.urls import path
from . import views

urlpatterns = [
    path('', views.BooksView.as_view()),
    path('<int:id>/', views.SingleBookView.as_view()),
]