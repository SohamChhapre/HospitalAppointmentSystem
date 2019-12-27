from django.shortcuts import render
from .models import Hospital
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .serializers import HospitalSerializer
# Create your views here.

class ListHospital(APIView):


    def get(self, request, format=None, id=None):
        request = self.request
        if id is None:
            queryset = Hospital.objects.all()
            serializer = HospitalSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            queryset = Hospital.objects.filter(User=id).first()
            serializer = HospitalSerializer(queryset, many=False)
            if queryset is None:
                return Response({"details":"Invalid User Id"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, id, format=None):
        query = self.get_hospital(id)
        serializer = HospitalSerializer(query, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

