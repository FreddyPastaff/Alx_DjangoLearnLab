from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.generics import ListAPIView
from .models import Book
from .serializers import BookSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser

# API Authentication and Permissions applied to views

class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]  # or IsAdminUser for admin-only access

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated] # or IsAdminUser for admin-only access