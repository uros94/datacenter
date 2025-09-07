from django.test import TestCase

from inventory.models import Device, Rack
from inventory.assignment import balanced_assignment

"""Za funkcionalnost davanja predloga rasporeda uređaja po rack-ovima potrebno je napisati
integration ili unit testove. Testovi za ostale funkcionalnosti nisu obavezni."""
class AssignmentTests(TestCase):
    def setUp(self):
        self.r1 = Rack.objects.create(
            name="R1", serial_number="R1", max_units=42, max_power_watts=5000
        )
        self.r2 = Rack.objects.create(
            name="R2", serial_number="R2", max_units=42, max_power_watts=5000
        )
        self.d1 = Device.objects.create(
            name="D1", serial_number="D1", units=1, power_watts=200
        )
        self.d2 = Device.objects.create(
            name="D2", serial_number="D2", units=2, power_watts=400
        )
        self.d3 = Device.objects.create(
            name="D3", serial_number="D3", units=3, power_watts=700
        )
        self.d4 = Device.objects.create(
            name="D4", serial_number="D4", units=4, power_watts=1000
        )
        self.d5 = Device.objects.create(
            name="D5", serial_number="D5", units=5, power_watts=1200
        )
        self.d6 = Device.objects.create(
            name="D6", serial_number="D6", units=3, power_watts=700
        )

    def test_balanced_assignment(self):
        devices = [self.d1, self.d2, self.d3, self.d4, self.d5, self.d6]
        racks = [self.r1, self.r2]

        print(f"\nTry assigning devices {devices} \nTo racks {racks}")
        assignments, unassigned_devices = balanced_assignment(devices, racks)
        if assignments:
            print("\nNew assignments:")
        for a in assignments:
            print(a)
        if unassigned_devices:
            print("\nUnassigned devices:")
        for d in unassigned_devices:
            print(d)

    def test_failed_assignment(self):
        dx = Device.objects.create(
            name="X", serial_number="X", units=5, power_watts=11200
        )
        racks = [self.r1, self.r2]

        print(f"\nTry assigning devices {[dx]} \nTo racks {racks}")
        assignments, unassigned_devices = balanced_assignment([dx], racks)
        if assignments:
            print("\nNew assignments:")
        for a in assignments:
            print(a)
        if unassigned_devices:
            print("\nUnassigned devices:")
        for d in unassigned_devices:
            print(d)
