from django.shortcuts import render
from rest_framework.generics import  CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth import get_user_model

User = get_user_model()

from .serializers import RegisterSerializer


class RegisterView(CreateAPIView):
    """
    View for Signup
    """
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny, ]
    queryset = User.objects.all()

    # def create(self, request, *args, **kwargs):