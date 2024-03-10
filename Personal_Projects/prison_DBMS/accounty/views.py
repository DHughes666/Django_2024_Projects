from rest_framework import viewsets
from .models import Inmate, Staff
from .serializers import InmateSerializer, StaffSerializer

# Create your views here.
class InmateViewSet(viewsets.ModelViewSet):
    queryset = Inmate.objects.all()
    serializer_class = InmateSerializer

class StaffViewSet(viewsets.ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
