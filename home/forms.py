from django.forms import ModelForm
from .models import WeatherStations
from django import forms

#modelform
class SolarPanelForm2(ModelForm):
    class Meta:
        model = WeatherStations
        fields = '__all__'

#regular form
class SolarPanelForm(forms.Form):
    #size,azimuth,tilt,bill,location
    size = forms.IntegerField()
    azimuth = forms.IntegerField()
    tilt = forms.IntegerField()
    bill = forms.DecimalField()

