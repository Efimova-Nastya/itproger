from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page, name='main'),
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),
    path('book/<int:book_id>/toggle-read/', views.toggle_read, name='toggle_read'),
    path('read/', views.read_books_page, name='read_books'),
    path('register/', views.register, name='register'),
    path('comment/<int:comment_id>/edit/', views.edit_comment, name='edit_comment'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
]