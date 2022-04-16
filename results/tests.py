from django.test import TestCase
from results.models import WeatherStation
from django.test import TestCase
from datetime import date, timedelta

# Create your tests here.
#Test to check whether a weather station is pulled from the DB 
class ModelTestCase(TestCase):
    def setUp(self):
        #this doesn't use the real db - so need to create some dummy data
        days = []
        for i in range(10):
            sdate = date(2012+i, 1, 1)
            dates = [sdate+timedelta(days=x) for x in range(12)]
            for a_date in dates:
                days.append(a_date.strftime("%Y-%m-%d"))

        for i in range(116):
            WeatherStation.objects.create(LOCATION="TESTING-STATION", DATE=days[i], GLORAD=50000, meant=10, maxtp=10,
            mintp=10, mnmax=10, mnmin=10, rain=10, gmin=10, wdsp=10, maxgt=10)

    #This will pass - station is in validation functions allowed list of stations
    def test_station_location_pass(self):
        station = 'TESTING-STATION'
        data = list(WeatherStation.objects.filter(LOCATION=station).values())
        self.assertGreaterEqual(len(data), 1)

    #This will fail - station is not in allowed list of stations 
    def test_station_location_fail(self):
        station = "invalid_location"
        data = list(WeatherStation.objects.filter(LOCATION=station).values())
        self.assertLess(len(data), 1)

class ResultsPageTestCase(TestCase):
    def setUp(self):
        #this doesn't use the real db - so need to create some dummy data
        days = []
        for i in range(10):
            sdate = date(2012+i, 1, 1)
            dates = [sdate+timedelta(days=x) for x in range(12)]
            for a_date in dates:
                days.append(a_date.strftime("%Y-%m-%d"))

        for i in range(116):
            WeatherStation.objects.create(LOCATION="TESTING-STATION", DATE=days[i], GLORAD=50000, meant=10, maxtp=10,
            mintp=10, mnmax=10, mnmin=10, rain=10, gmin=10, wdsp=10, maxgt=10)

    #Results page tests
    def test_results_page_view_get(self):
        response = self.client.get('/results')
        self.assertEqual(type(response).__name__, 'HttpResponseRedirect')

    def test_results_page_view_post(self):
        response = self.client.post('/results', data={'location_input': 'TESTING-STATION', 'location_name': 'TESTING-STATION', 'size':0.25, 'azimuth':'S', 'tilt':'15'})
        self.assertEqual(response.status_code, 200)

    def test_results_page_template(self):
        response = self.client.post('/results', data={'location_input': 'TESTING-STATION', 'location_name': 'TESTING-STATION', 'size':0.25, 'azimuth':'S', 'tilt':'15'})
        self.assertTemplateUsed(response, 'results/results.html')
    
    #test that after going to results, then leaving that page, when going back to it the data is still there
    def test_results_page_context(self):
        response = self.client.post('/results', data={'location_input': 'TESTING-STATION', 'location_name': 'TESTING-STATION', 'size':0.25, 'azimuth':'S', 'tilt':'15'})
        response2 = self.client.get('/')
        response3 = self.client.get('/results')
        self.assertGreater(len(response3.context['yearly_vals']['yearly_KwH']), 0)
        self.assertTemplateUsed(response3, 'results/results.html')
