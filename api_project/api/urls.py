from django.urls import path, include
from .views import BookList, BookViewSet, BookViewset
from rest_framework.routers import DefaultRouter
from rest_framework.authentication import obtain_auth_token

router = DefaultRouter()
router.register(r'books', BookViewSet, basename='book')

urlpatterns = [
    path('books/', BookList.as_view(), name='book-list'),
    path('', include(router.urls)),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]