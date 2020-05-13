""" Users views """

# Django REST Framework
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView 

# Serializers
from cride.users.serializers import (
    UserLoginSerializer,
    UserModelSerializer
)


class UserLoginAPIView(APIView):
    """User Login API View"""
    
    def post(self, request, *args, **kwargs):
        """Handle HTTP POST request """
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        data = {
            'user': UserModelSerializer(user).data,
            'acces_token': token
        }
        return Response(data, status=status.HTTP_201_CREATED)