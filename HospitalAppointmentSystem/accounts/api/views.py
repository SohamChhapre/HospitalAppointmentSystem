from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import permissions,status
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
            context = {
                    "message":"Hospital's Data",
                    "status":True,
                    "data":{
                            'token': str(token[0]),
                            'email': user.email,
                            'name': user.full_name,
                            'id': user.id
                            }
                    }
            return Response(context,status=status.HTTP_202_ACCEPTED)
        else:
            context = {
                    "message":"You are not authenticated!!",
                    "status":False,
                    "data":None
                    }
            return Response(context,status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)