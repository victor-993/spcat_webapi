import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
from api import app
from ormgap import Crop, Group, Accession
from mongoengine import connect

class AccessionsByIDCropTestCase(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        connect('test_gap_analysis', host='mongomock://localhost')
        cls.crop1 = Crop(name='Crop1', ext_id='1', base_name='BaseName1', app_name='AppName1').save()
        cls.crop2 = Crop(name='Crop2', ext_id='2', base_name='BaseName2', app_name='AppName2').save()

        cls.group1 = Group(group_name='Group1', ext_id='1', crop=cls.crop1).save()
        cls.group2 = Group(group_name='Group2', ext_id='2', crop=cls.crop1).save()

        cls.group3 = Group(group_name='Group3', ext_id='3', crop=cls.crop2).save()
        cls.group4 = Group(group_name='Group4', ext_id='4', crop=cls.crop2).save()

        cls.accession1 = Accession(species_name='Test species 1', institution_name='Test institution 1',
                                    latitude=1.0, longitude=1.0, ext_id='Test ext ID 1', 
                                    crop= cls.crop1, landrace_group=cls.group1, 
                                    accession_id='Test accession ID 1', other_attributes={'Test attribute': 'Test value'})
        cls.accession1.save()

        cls.accession2 = Accession(species_name='Test species 2', institution_name='Test institution 2',
                                    latitude=2.0, longitude=2.0, ext_id='Test ext ID 2',
                                    crop= cls.crop1, landrace_group=cls.group1,
                                    accession_id='Test accession ID 2', other_attributes={'Test attribute': 'Test value'})
        cls.accession2.save()

        cls.accession3 = Accession(species_name='Test species 3', institution_name='Test institution 3',
                                    latitude=2.0, longitude=2.0, ext_id='Test ext ID 3',
                                    crop= cls.crop1, landrace_group=cls.group2, 
                                    accession_id='Test accession ID 3', other_attributes={'Test attribute': 'Test value'})
        cls.accession3.save()

        cls.accession4 = Accession(species_name='Test species 4', institution_name='Test institution 4',
                                    latitude=2.0, longitude=2.0, ext_id='Test ext ID 4',
                                    crop= cls.crop2, landrace_group=cls.group3, 
                                    accession_id='Test accession ID 4', other_attributes={'Test attribute': 'Test value'})
        cls.accession4.save()

        cls.accession5 = Accession(species_name='Test species 5', institution_name='Test institution 5',
                                    latitude=2.0, longitude=2.0, ext_id='Test ext ID 5',
                                    crop= cls.crop2, landrace_group=cls.group4, 
                                    accession_id='Test accession ID 5', other_attributes={'Test attribute': 'Test value'})
        cls.accession5.save()

        cls.app = app.test_client()

    @classmethod
    def tearDownClass(cls):
        Crop.drop_collection()
        Group.drop_collection()

    def test_get_accession_by_crop_id(self):
        # Test with single valid crop id
        response = self.app.get('/api/v1/accessionsbyidcrop?id=' + str(self.crop1.id))        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 3)
        self.assertEqual(response.json[0]['species_name'], 'Test species 1')
        self.assertEqual(response.json[0]['ext_id'], 'Test ext ID 1')
        self.assertEqual(response.json[0]['crop'], str(self.crop1.id))
        self.assertEqual(response.json[1]['species_name'], 'Test species 2')
        self.assertEqual(response.json[1]['ext_id'], 'Test ext ID 2')
        self.assertEqual(response.json[1]['crop'], str(self.crop1.id))

        # Test with multiple valid crop ids
        response = self.app.get('/api/v1/accessionsbyidcrop?id=' + str(self.crop1.id) + ',' + str(self.crop2.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 2)
        self.assertEqual(response.json[0]['accessions'][0]['species_name'], 'Test species 1')
        self.assertEqual(response.json[0]['accessions'][0]['ext_id'], 'Test ext ID 1')
        self.assertEqual(response.json[0]['accessions'][0]['crop'], str(self.crop1.id))
        self.assertEqual(response.json[1]['accessions'][0]['species_name'], 'Test species 4')
        self.assertEqual(response.json[1]['accessions'][0]['ext_id'], 'Test ext ID 4')
        self.assertEqual(response.json[1]['accessions'][0]['crop'], str(self.crop2.id))

        # Test with invalid crop id
        response = self.app.get('/api/v1/accessionsbyidcrop?id=invalid_id')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['message'], 'Invalid crop ID')

        response = self.app.get('/api/v1/accessionsbyidcrop?id=640961b88e2f0a8574155555')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['error'], 'Crop with id 640961b88e2f0a8574155555 not found')

    def test_get_accession_by_group_id(self):
        # Test with single valid group id
        response = self.app.get('/api/v1/accessionsbyidgroup?id=' + str(self.group1.id))        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 2)
        self.assertEqual(response.json[0]['species_name'], 'Test species 1')
        self.assertEqual(response.json[0]['ext_id'], 'Test ext ID 1')
        self.assertEqual(response.json[0]['landrace_group'], str(self.group1.id))
        self.assertEqual(response.json[1]['species_name'], 'Test species 2')
        self.assertEqual(response.json[1]['ext_id'], 'Test ext ID 2')
        self.assertEqual(response.json[1]['landrace_group'], str(self.group1.id))

        # Test with multiple valid group ids
        response = self.app.get('/api/v1/accessionsbyidgroup?id=' + str(self.group1.id) + ',' + str(self.group2.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 2)
        self.assertEqual(response.json[0]['accessions'][0]['species_name'], 'Test species 1')
        self.assertEqual(response.json[0]['accessions'][0]['ext_id'], 'Test ext ID 1')
        self.assertEqual(response.json[0]['accessions'][0]['landrace_group'], str(self.group1.id))
        self.assertEqual(response.json[1]['accessions'][0]['species_name'], 'Test species 3')
        self.assertEqual(response.json[1]['accessions'][0]['ext_id'], 'Test ext ID 3')
        self.assertEqual(response.json[1]['accessions'][0]['landrace_group'], str(self.group2.id))

        # Test with invalid crop id
        response = self.app.get('/api/v1/accessionsbyidgroup?id=invalid_id')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['message'], 'Invalid group ID')

        response = self.app.get('/api/v1/accessionsbyidgroup?id=640961b88e2f0a8574155555')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['error'], 'Group with id 640961b88e2f0a8574155555 not found')

if __name__ == '__main__':
    unittest.main()