# Import necessary modules and classes from Django and REST framework
from django.shortcuts import render
from django.db.models import Count
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from .serializer import ServerSerializer
from .models import Server

# Define a class for handling server list view set
class ServerListViewSet(viewsets.ViewSet):
    # Set the queryset to include all Server objects
    queryset = Server.objects.all()

    # Define a method to handle GET requests for listing servers
    def list(self, request):
        # Extract query parameters from the request
        category = request.query_params.get('category')
        qty = request.query_params.get('qty')
        by_user = request.query_params.get('by_user') == 'true'
        by_serverId = request.query_params.get('by_serverId')
        with_num_members = request.query_params.get('with_num_members') == 'true'

        # Check authentication for user-specific queries
        if by_user or by_serverId and not request.user.is_authenticated:
            raise AuthenticationFailed()

        # Apply filters based on query parameters
        if category:
            # Filter by category (either category id or category name)
            self.queryset = self.queryset.filter(category=category)
            # Uncomment the line below to filter by category name
            # self.queryset = self.queryset.filter(category__name=category)

        if by_user:
            # Filter servers based on the requesting user
            user_id = request.user.id
            self.queryset = self.queryset.filter(member=user_id)

        if qty:
            # Limit the queryset to a specified quantity
            self.queryset = self.queryset[:int(qty)]

        if with_num_members:
            # Annotate the queryset with the count of members for each server
            self.queryset = self.queryset.annotate(num_members=Count("member"))

        if by_serverId:
            try:
                # Filter servers by a specific server ID
                self.queryset = self.queryset.filter(id=by_serverId)
                # Raise a validation error if the server with the given ID does not exist
                if not self.queryset.exists():
                    raise ValidationError(
                        detail=f"Server with id {by_serverId} not found")
            except ValueError:
                # Raise a validation error if the provided server ID is not valid
                raise ValidationError(
                    detail=f"Server with id {by_serverId} does not exist")

        # Create context data to be passed to the serializer
        context = {"num_members": with_num_members}
        # Serialize the queryset using the ServerSerializer
        serializer = ServerSerializer(
            self.queryset, many=True, context=context)
        # Return the serialized data in the HTTP response
        return Response(serializer.data)
