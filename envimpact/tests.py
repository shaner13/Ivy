from django.test import TestCase
from results.models import WeatherStation
from django.test import TestCase
from datetime import date, timedelta

# Create your tests here.
class EnvImpactTestCase(TestCase):
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

    #Environmental Impact page tests
    def test_envimpact_page_view_get(self):
        response = self.client.get('/envimpact')
        self.assertEqual(type(response).__name__, 'HttpResponseRedirect')

    def test_envimpact_page_view_post(self):
        response = self.client.post('/results', data={'location_input': 'TESTING-STATION', 'location_name': 'TESTING-STATION', 'size':0.25, 'azimuth':'S', 'tilt':'15'})
        response2 = self.client.get('/envimpact')
        print(response2.content)
        self.assertEqual(response2.status_code, 200)

    def test_envimpact_page_view_post(self):
        response = self.client.post('/results', data={'location_input': 'TESTING-STATION', 'location_name': 'TESTING-STATION', 'size':0.25, 'azimuth':'S', 'tilt':'15'})
        response2 = self.client.get('/envimpact')
        self.assertTemplateUsed(response2, 'envimpact/envimpact.html')

    #test that after going to environental impact, then leaving that page, when going back to it the data is still there
    def test_envimpact_page_context(self):
        response = self.client.post('/results', data={'location_input': 'TESTING-STATION', 'location_name': 'TESTING-STATION', 'size':0.25, 'azimuth':'S', 'tilt':'15'})
        response2 = self.client.get('/')
        response3 = self.client.get('/envimpact')
        self.assertGreater(len(response3.context['co2_reduction']), 0)
        self.assertTemplateUsed(response3, 'envimpact/envimpact.html')