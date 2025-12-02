from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.generics import ListAPIView
from .models import Book
from .serializers import BookSerializer

class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.object.all()
    serializer_class = BookSerializer
