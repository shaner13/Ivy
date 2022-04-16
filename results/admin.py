from django.contrib import admin

from results.models import WeatherStation

from import_export.admin import ImportExportModelAdmin

# Register your models here.


class WeatherStationsAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'LOCATION', 'DATE', 'GLORAD', 'meant', 'maxtp', 'mintp', 'mnmax', 'mnmin', 'rain', 'gmin', 'wdsp', 'maxgt')

admin.site.register(WeatherStation, WeatherStationsAdmin)
