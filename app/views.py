from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import authentication, permissions
from app.serializers import *
from todoapp.models import Todos


class TodosView(ModelViewSet):
    # queryset = Todos.objects.all() #It is the default query set Must be given otherwise get_query functin
    serializer_class = TodoSerializer

    # authentication_classes = [authentication.BasicAuthentication]   # MY api worked even this lines commented.But basic auth details must be provided
    # permission_classes = [permissions.IsAuthenticated]

    # 'TodosView' should either include a `queryset` attribute, or override the `get_queryset()` method.

    def get_queryset(self): # It's for making our own query. I cannot make new query to queryset above,bcs self won't work there
        return Todos.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs): #its for passinf context to serialize
        serializer = TodoSerializer(data=request.data,context={"user":request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.data)

