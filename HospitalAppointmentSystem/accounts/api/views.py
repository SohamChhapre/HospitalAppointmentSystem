from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import permissions
from django.contrib.auth import authenticate,get_user_model
from .serializers import UserRegisterSerializer
from .permissions import AnonPermissionOnly

class CustomAuthToken(ObtainAuthToken):

    permission_classes     = [AnonPermissionOnly]
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token = Token.objects.get_or_create(user=user)
        if user.is_hospital:
            return Response({
                'token': str(token[0]),
                'email': user.email,
                'name': user.full_name,
                'id': user.id
            })
        else:
            return Response({'Details':'You are not authenticated!!'})