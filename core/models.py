from django.db import models

# Create your models here.
class Planet(models.Model):
    name = models.CharField(max_length=50) # name of planet
    a = models.FloatField() # semi-major axis
    ecc = models.FloatField() # eccentricity
    p = models.FloatField() # period of orbit
    modified_p = models.FloatField() # p relative to either Earth or Jupiter
    beta = models.FloatField() # angle of inclination of orbit

    def __str__(self):
        return self.name
