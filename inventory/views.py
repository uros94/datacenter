from django.db.models.expressions import result
from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, status
from django.db.models import Prefetch, QuerySet

from .assignment import balanced_assignment
from .models import Device, Rack, DeviceAssignment
from .serializers import DeviceSerializer, RackSerializer, DeviceAssignmentSerializer

"""Potrebno je razviti aplikaciju koja korisnicima putem REST API-ja omogućava pristup definisanim
funkcionalnostima. Nije neophodno implementirati sistem autentifikacije, autorizacije niti
upravljanje korisnicima kao entitetima – fokus treba da bude isključivo na gore navedenim
entitetima i njihovim funkcionalnostima."""
# joint device CRUD operations using ModelViewSet
class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

# joint rack CRUD operations using ModelViewSet
class RackViewSet(viewsets.ModelViewSet):
    queryset = Rack.objects.all().prefetch_related(
        Prefetch('assignments', queryset=DeviceAssignment.objects.select_related('device'))
    )
    serializer_class = RackSerializer

# joint deviceAssignment CRUD operations using ModelViewSet + custom assign request
class DeviceAssignmentViewSet(viewsets.ModelViewSet):
    queryset = DeviceAssignment.objects.select_related('device','rack')
    serializer_class = DeviceAssignmentSerializer

    @action(detail=False, methods=['post'], url_path='assign')
    def assign(self, request):
        device_ids = request.data.get('device_ids', [])
        rack_ids = request.data.get('rack_ids', [])

        devices = Device.objects.filter(id__in=device_ids)
        racks = Rack.objects.filter(id__in=rack_ids)
        print("\nINPUT\n",devices,racks)

        assignments, unassigned_devices = balanced_assignment(devices, racks)
        print("\nASSIGNMENTS\n",assignments)

        assignments_serializer = DeviceAssignmentSerializer(assignments, many=True)
        unassigned_serializer = DeviceSerializer(unassigned_devices, many=True)
        racks_serializer = RackSerializer(racks, many=True)

        return Response(
            {
                "assignments": assignments_serializer.data,
                "unassigned_devices": unassigned_serializer.data,
                "racks": racks_serializer.data
            },
            status=status.HTTP_200_OK
        )