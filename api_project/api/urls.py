from django.urls import path, include
from .views import BookList, BookViewset
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'books', BookViewset, basename='book')

urlpatterns = [
    path('books/', BookList.as_view(), name='book-list'),
    path('', include(router.urls)),
]