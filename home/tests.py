from django.test import TestCase
from results.models import WeatherStation
from django.test import TestCase
from datetime import date, timedelta

# Create your tests here.
class HomePageTestCase(TestCase):
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

    #Home page tests
    def test_home_page_view(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_home_page_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home/home.html')