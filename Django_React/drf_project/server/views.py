from django.shortcuts import render
from rest_framework import viewsets

from .models import Server

# Create your views here.
class ServerListViewSet(viewsets.ViewSet):

    queryset = Server.objects.all()

    def list(self, request):
        category = request.query_params.get('category')

        if category:
            self.queryset.filter(category = category)

        