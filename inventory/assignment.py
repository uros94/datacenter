from http.client import responses

from yaml import serialize

from .models import Device, Rack, DeviceAssignment
from .serializers import DeviceAssignmentSerializer
from typing import List

"""razviti fukcionalnost kojom je omogućeno korisniku da unese određene uređaje
i rack-ove gde će kao output biti prikazan balansiran raspored datih uređaja po datim rack-
ovima. Kao ishod ovakvog raspoređivanja potrebno je da svaki rack u nizu ima što približnije
procentualno istu iskorišćenost maksimalne deklarisane potrošnje el. Energije (0%-100%).
Imajući u vidu ovakve zahteve potrebno je implementirati algoritam, na sopstveni način i po
sopstvenoj proceni, tako da se u što većoj meri ispune ovi zahtevi."""
def balanced_assignment(devices: List[Device], racks:List[Rack]):
    assignments = []
    unassigned_devices = list(devices)
    sorted_devices = sorted(devices, key=lambda d: -d.power_watts)
    for device in sorted_devices:

        sorted_racks = sorted(racks, key=lambda r: r.utilization)
        for rack in sorted_racks:
            assign_data = {
                'device': device.id,
                'rack': rack.id
            }

            serializer = DeviceAssignmentSerializer(data=assign_data)
            if serializer.is_valid():
                new_ass = serializer.save()
                assignments.append(new_ass)
                unassigned_devices.remove(device)
                break
            else:
                print(serializer.errors)

    return assignments, unassigned_devices