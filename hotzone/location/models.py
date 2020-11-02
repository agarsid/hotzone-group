from django.db import models

# Create your models here.
class Locations(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    x_coord = models.FloatField()
    y_coord = models.FloatField()
    def __str__(self):
        return self.name