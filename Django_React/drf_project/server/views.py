from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets
from .serializer import ServerSerializer

from .models import Server

# Create your views here.
class ServerListViewSet(viewsets.ViewSet):

    queryset = Server.objects.all()

    def list(self, request):
        category = request.query_params.get('category')

        if category:
            self.queryset.filter(category = category)

        serializer = ServerSerializer(self.queryset, many=True)
        return Response(serializer.data)

        