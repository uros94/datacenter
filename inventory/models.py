from django.db import models
from django.core.validators import MinValueValidator

"""Ovaj entitet predstavlja uređaj (server, switch...) koji se koristi u infrastrukturi data
centra, i potreno je da ima ime, opis, serijski broj, broj jedinica koji zauzima u okviru rack-a
(1+, samo prirodni brojevi) i potrošnju el. energije izraženu u Vatima (300W, 500W,
1200W...)."""
class Device(models.Model):
    name = models.CharField(max_length=60)
    description = models.TextField(blank=True)
    serial_number = models.CharField(max_length=60)
    units = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    power_watts = models.PositiveIntegerField()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return (f"{self.name}, {self.serial_number}, "
                f"{self.units} units, power {self.power_watts}W")

"""Uređaji u data centru postavljaju se u rack, kojih može biti više. Rack treba da ima
ime, opis, serijski broj i broj jedinica/units (42U, 48U...) koji može da podrži, kao i
maksimalnu deklarisanu potrošnju el. energije koju može da podrži(5000W+), gde zbir
potrošnje svih uređaja u rack-u ne sme da bude veći od ukupne deklarisane potrošnje koji
rack pruža."""   
class Rack(models.Model):
    name = models.CharField(max_length=60)
    description = models.TextField(blank=True)
    serial_number = models.CharField(max_length=60)
    max_units = models.PositiveIntegerField()
    max_power_watts = models.PositiveIntegerField()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return (f"{self.name}, {self.serial_number}, "
                f"units {self.used_units}/{self.max_units}, "
                f"power {self.used_power_watts}/{self.max_power_watts}W "
                f"(utilization {self.utilization}%)")

    def print_devices(self):
        return self.assignments.select_related('device')

    @property
    def used_units(self):
        return sum(dev.device.units for dev in self.assignments.select_related('device'))

    """Pri dohvatanju rack-a potrebno je pored ukupnog kapaciteta za potrošnju energije prikazati i
koliko ukupno troše uređaji na istom."""
    @property
    def used_power_watts(self):
        return sum(dev.device.power_watts for dev in self.assignments.select_related('device'))

    @property
    def utilization(self):
        if self.max_power_watts == 0:
            return 0.0
        return round(100.0 * self.used_power_watts / self.max_power_watts)

class DeviceAssignment(models.Model):
    device = models.OneToOneField(
        Device, on_delete=models.CASCADE, related_name='assignment'
    )
    rack = models.ForeignKey(
        Rack, on_delete=models.CASCADE, related_name='assignments'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [('device','rack')]
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.device} --- rack: {self.rack}"



