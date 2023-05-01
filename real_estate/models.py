from django.db import models


class Property(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(default=None, null=True)
    source = models.CharField(max_length=64, blank=False, null=False)
    source_id = models.CharField(max_length=64, blank=False, null=False, unique=True)
    available = models.BooleanField(default=False)
    apartment_type = models.CharField(max_length=32, blank=True, null=True)
    rooms = models.CharField(max_length=32, blank=True, null=True)
    floor = models.CharField(max_length=32, blank=True, null=True)
    area_size = models.FloatField(blank=True, null=True)
    area_total_size = models.FloatField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
