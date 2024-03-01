from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from .serializer import ServerSerializer

from .models import Server

# Create your views here.
class ServerListViewSet(viewsets.ViewSet):

    queryset = Server.objects.all()

    def list(self, request):
        category = request.query_params.get('category')
        qty = request.query_params.get('qty')
        by_user = request.query_params.get('by_user') == 'true'
        by_serverId = request.query_params.get('by_serverId')

        if category:
            # Sort by category id
            self.queryset = self.queryset.filter(category = category)
            # Sort by category name
            # self.queryset = self.queryset.filter(category__name = category)
        
        if by_user:
            user_id = request.user.id
            self.queryset = self.queryset.filter(member = user_id)

        if qty:
            self.queryset = self.queryset[: int(qty)]

        if by_serverId:
            try:
                self.queryset = self.queryset.filter(id = by_serverId)
                if not self.queryset.exists():
                    raise ValidationError(
                        detail=f"Server with id {by_serverId} not found")
            except ValueError:
                raise ValidationError(
                    detail=f"Server with id {by_serverId} does not exist")

        serializer = ServerSerializer(self.queryset, many=True)
        return Response(serializer.data)

        