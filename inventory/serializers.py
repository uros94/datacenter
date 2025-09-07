from django.middleware.gzip import re_accepts_gzip
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Device, Rack, DeviceAssignment

# Device model to JSON serializer
class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ['id', 'name', 'description', 'serial_number',
                  'units', 'power_watts']

# Rack model to JSON serializer
class RackSerializer(serializers.ModelSerializer):
    used_units = serializers.IntegerField(read_only=True)
    used_power_watts = serializers.IntegerField(read_only=True)
    utilization = serializers.FloatField(read_only=True)

    class Meta:
        model = Rack
        fields = ['id', 'name', 'description', 'serial_number',
                  'max_units', 'max_power_watts',
                  'used_units', 'used_power_watts', 'utilization']

# DeviceAssignment model to JSON serializer
class DeviceAssignmentSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = DeviceAssignment
        fields = ['id', 'device', 'rack', 'created_at']

    """obraditi greške ukoliko više nema mesta za sve uređaje u nekom ili ni u jednom
    rack-u, i zaključiti gde je potrebno prikazivati validacionu grešku,"""
    def validate(self, attrs):
        device = attrs['device']
        rack = attrs['rack']

        # already exists
        if DeviceAssignment.objects.filter(device=device).exists():
            raise ValidationError(f"Device {device} already assigned to {rack}")

        # not enough units available in the rack
        new_units = rack.used_units + device.units
        if new_units > rack.max_units:
            raise ValidationError(f"Device {device} requires more available units than {rack} has.")

        # power exceeded
        new_power = rack.used_power_watts + device.power_watts
        if new_power > rack.max_power_watts:
            raise ValidationError(f"Device {device} requires more power than {rack} has available.")

        return attrs