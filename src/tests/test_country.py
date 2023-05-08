import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
from api import app
from ormgap import Country
from mongoengine import connect

class CountriesEndpointTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        connect('test_gap_analysis', host='mongomock://localhost')
        Country.drop_collection()
        cls.country1 = Country(name='Colombia', iso_2='CO').save()
        cls.country2 = Country(name='United States', iso_2='US').save()
        cls.country3 = Country(name='Canada', iso_2='CA').save()
        cls.app = app.test_client()

    @classmethod
    def tearDownClass(cls):
        Country.drop_collection()

    def test_get_countries(self):
        response = self.app.get('/api/v1/countries')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 3)
        self.assertEqual(response.json[0]['name'], 'Colombia')
        self.assertEqual(response.json[1]['name'], 'United States')
        self.assertEqual(response.json[2]['name'], 'Canada')


if __name__ == '__main__':
    unittest.main()