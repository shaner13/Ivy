from django.db import models
from django.core.exceptions import ValidationError

#validator for station
def validateStation(value):
    stations = ['MALIN HEAD', 'BIRR', 'CLONES', 'BELMULLET', 'VALENTIA OBSERVATORY', 'DUBLIN AIRPORT']
    if "value" in stations:
        return value
    else:
        raise ValidationError("Invalid station sent.")



# Create your models here.
class WeatherStation(models.Model):
    LOCATION = models.CharField(max_length=50, validators =[validateStation])
    DATE = models.DateField()
    GLORAD = models.FloatField()
    meant = models.FloatField()
    maxtp = models.FloatField()
    mintp = models.FloatField()
    mnmax = models.FloatField()
    mnmin = models.FloatField()
    rain = models.FloatField()
    gmin = models.FloatField()
    wdsp = models.FloatField()
    maxgt = models.FloatField()