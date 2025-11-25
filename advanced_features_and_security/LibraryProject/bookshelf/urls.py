from django.urls import path
from .views import example_form_view, book_list_view

urlpatterns = [
    path("form/", example_form_view, name="example-form"),
    path("books/", book_list_view, name="book-list"),
]