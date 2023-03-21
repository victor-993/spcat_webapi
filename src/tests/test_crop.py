import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
from api import app
from ormgap import Crop, Group
from mongoengine import connect

class TestCropsEndpoint(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        connect('test_gap_analysis', host='mongomock://localhost')
        cls.crop1 = Crop(name='Crop1', ext_id='1', base_name='BaseName1', app_name='AppName1').save()
        cls.crop2 = Crop(name='Crop2', ext_id='2', base_name='BaseName2', app_name='AppName2').save()
        cls.crop3 = Crop(name='Crop3', ext_id='3', base_name='BaseName3', app_name='AppName3').save()
        cls.app = app.test_client()

    @classmethod
    def tearDownClass(cls):
        Crop.drop_collection()


    def setUp(self):
        self.app = app.test_client()

    def test_get_all_crops(self):
        response = self.app.get('/api/v1/crops')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 3)
        self.assertEqual(response.json[0]['name'], 'Crop1')
        self.assertEqual(response.json[1]['name'], 'Crop2')
        self.assertEqual(response.json[2]['name'], 'Crop3')


class GroupsTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        connect('test_gap_analysis', host='mongomock://localhost')
        cls.crop = Crop(name='Crop1', ext_id='1', base_name='BaseName1', app_name='AppName1').save()
        cls.group1 = Group(group_name='Group1', ext_id='1', crop=cls.crop).save()
        cls.group2 = Group(group_name='Group2', ext_id='2', crop=cls.crop).save()
        cls.group3 = Group(group_name='Group3', ext_id='3', crop=cls.crop).save()
        cls.app = app.test_client()

    @classmethod
    def tearDownClass(cls):
        Group.drop_collection()
        Crop.drop_collection()

    def test_get_all_groups(self):
        response = self.app.get('/api/v1/groups')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 3)
        self.assertEqual(response.json[0]['group_name'], 'Group1')
        self.assertEqual(response.json[1]['group_name'], 'Group2')
        self.assertEqual(response.json[2]['group_name'], 'Group3')

class GroupsByIDCropTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        connect('test_gap_analysis', host='mongomock://localhost')
        cls.crop1 = Crop(name='Crop1', ext_id='1', base_name='BaseName1', app_name='AppName1').save()
        cls.crop2 = Crop(name='Crop2', ext_id='2', base_name='BaseName2', app_name='AppName2').save()
        cls.crop3 = Crop(name='Crop3', ext_id='3', base_name='BaseName3', app_name='AppName3').save()

        cls.group1 = Group(group_name='Group1', ext_id='1', crop=cls.crop1).save()
        cls.group2 = Group(group_name='Group2', ext_id='2', crop=cls.crop1).save()

        cls.group3 = Group(group_name='Group3', ext_id='3', crop=cls.crop2).save()
        cls.group4 = Group(group_name='Group4', ext_id='4', crop=cls.crop2).save()

        cls.group5 = Group(group_name='Group5', ext_id='5', crop=cls.crop3).save()
        cls.group6 = Group(group_name='Group6', ext_id='6', crop=cls.crop3).save()
        cls.app = app.test_client()

    @classmethod
    def tearDownClass(cls):
        Crop.drop_collection()
        Group.drop_collection()

    def test_get_groups_by_crop_id(self):
        # Test with single valid crop id
        response = self.app.get('/api/v1/groups?id=' + str(self.crop1.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 2)
        self.assertEqual(response.json[0]['group_name'], 'Group1')
        self.assertEqual(response.json[0]['ext_id'], '1')
        self.assertEqual(response.json[0]['crop'], str(self.crop1.id))
        self.assertEqual(response.json[1]['group_name'], 'Group2')
        self.assertEqual(response.json[1]['ext_id'], '2')
        self.assertEqual(response.json[1]['crop'], str(self.crop1.id))

        # Test with multiple valid crop ids
        response = self.app.get('/api/v1/groups?id=' + str(self.crop1.id) + ',' + str(self.crop2.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 2)
        self.assertEqual(response.json[0]['groups'][0]['group_name'], 'Group1')
        self.assertEqual(response.json[0]['groups'][0]['ext_id'], '1')
        self.assertEqual(response.json[0]['groups'][0]['crop'], str(self.crop1.id))
        self.assertEqual(response.json[1]['groups'][0]['group_name'], 'Group3')
        self.assertEqual(response.json[1]['groups'][0]['ext_id'], '3')
        self.assertEqual(response.json[1]['groups'][0]['crop'], str(self.crop2.id))
        
        # Test with invalid crop id
        response = self.app.get('/api/v1/groups?id=invalid_id')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['message'], 'Invalid crop ID')

        response = self.app.get('/api/v1/groups?id=640961b88e2f0a8574155555')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['error'], 'Crop with id 640961b88e2f0a8574155555 not found')

if __name__ == '__main__':
    unittest.main()