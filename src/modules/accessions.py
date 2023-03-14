from flask import Flask, jsonify, request
from flask_restful import Resource
from ormgap import Crop, Group, Accession
import re

def is_valid_object_id(value):
    """
    Returns True if `value` is a valid hexadecimal string representation of an ObjectId, False otherwise.
    """
    if not isinstance(value, str):
        return False
    pattern = re.compile("[0-9a-f]{24}")
    return pattern.match(value) is not None

class AccessionsByIDCrop(Resource):

    def __init__(self):
        super().__init__()

    def get(self):
        """
        Get accessions from database by crop id(s)
        ---
        parameters:
          - name: id
            in: path
            description: Crop id(s)
            required: true
            type: string
            example: 6035f5e5c6be2f14d07d6c7d or 6035f5e5c6be2f14d07d6c7d,6035f5e5c6be2f14d07d6c7e
        responses:
          200:
            description: 
            schema:
              id: Accession
              properties:
                id:
                  type: string
                  description: Id accession
                species_name: 
                  type: string
                  description: Name of the species of the accession.
                crop: 
                  type: string
                  description: Id crop that the accession belongs to.
                landrace_group:
                  type: string
                  description: Id group that the group belongs to.
                institution_name: 
                  type: string
                  description: Name of the institution that holds the accession.
                source_database: 
                  type: string
                  description: Name of the database where the accession was originally stored. Optional.
                latitude: 
                  type: float
                  description: Latitude of the geographical location where the accession was collected.
                longitude: 
                  type: float
                  description: Longitude of the geographical location where the accession was collected.
                accession_id:
                  type: string
                  description: The identifier of the accession in source database.
                ext_id: 
                  type: string
                  description: External identifier for the accession.
                other_attributes: 
                  type: dict
                  description: Additional attributes of the accession.
        """
        
        # If id is a list of ids, return groups for each crop
        id = request.args.get('id')

        if id is not None:
            id_list = id.split(',')

            print(id)
            if len(id_list) == 1:
                if is_valid_object_id(id):
                    # Case 2: Single id provided, list accession for that crop
                    crop = Crop.objects(id=id).first()
                    if crop is None:
                        return jsonify({"error": "Crop not found"}), 404
                    accessions = Accession.objects(crop=crop)
                    json_data = [{"id": str(x.id), "species_name": x.species_name,
                                "ext_id": x.ext_id, "crop": str(x.crop.id),
                                "landrace_group":str(x.landrace_group.id), 
                                "institution_name":x.institution_name,
                                "source_database":x.source_database,
                                "latitude":x.latitude,
                                "longitude":x.longitude,
                                "accession_id":x.accession_id}
                                for x in accessions]
                    return json_data
                else:
                    return {'message': 'Invalid crop ID'}, 400
            else:
                # Case 3: List of ids provided, list accession for each crop separately
                json_data = []
                for crop_id in id_list:     
                    if is_valid_object_id(crop_id):
                        crop = Crop.objects(id=crop_id).first()
                        if crop is None:
                            json_data.append({"error": f"Crop with id {crop_id} not found"})
                        else:
                            accessions = Accession.objects(crop=crop)
                            crop_data = {"crop_id": str(crop.id),
                                        "accessions": [{"id": str(x.id), "species_name": x.species_name,
                                                        "ext_id": x.ext_id, "crop": str(x.crop.id),
                                                        "landrace_group":str(x.landrace_group.id), 
                                                        "institution_name":x.institution_name,
                                                        "source_database":x.source_database,
                                                        "latitude":x.latitude,
                                                        "longitude":x.longitude,
                                                        "accession_id":x.accession_id}
                                                        for x in accessions]}
                            json_data.append(crop_data)
                    else:
                        json_data.append({"crop_id": crop_id,"error": "Invalid crop ID"})
                return json_data
        else: 
            return {'message': 'Invalid crop ID'}, 400
        

class AccessionsByIDGroup(Resource):

    def __init__(self):
        super().__init__()

    def get(self):
        """
        Get accessions from database by group id(s)
        ---
        parameters:
          - name: id
            in: path
            description: Group id(s)
            required: true
            type: string
            example: 6035f5e5c6be2f14d07d6c7d or 6035f5e5c6be2f14d07d6c7d,6035f5e5c6be2f14d07d6c7e
        responses:
          200:
            description: 
            schema:
              id: Accession
              properties:
                id:
                  type: string
                  description: Id accession
                species_name: 
                  type: string
                  description: Name of the species of the accession.
                crop: 
                  type: string
                  description: Id crop that the accession belongs to.
                landrace_group:
                  type: string
                  description: Id group that the group belongs to.
                institution_name: 
                  type: string
                  description: Name of the institution that holds the accession.
                source_database: 
                  type: string
                  description: Name of the database where the accession was originally stored. Optional.
                latitude: 
                  type: float
                  description: Latitude of the geographical location where the accession was collected.
                longitude: 
                  type: float
                  description: Longitude of the geographical location where the accession was collected.
                accession_id:
                  type: string
                  description: The identifier of the accession in source database.
                ext_id: 
                  type: string
                  description: External identifier for the accession.
                other_attributes: 
                  type: dict
                  description: Additional attributes of the accession.
        """
        
        # If id is a list of ids, return groups for each crop
        id = request.args.get('id')

        if id is not None:
            id_list = id.split(',')

            print(id)
            if len(id_list) == 1:
                if is_valid_object_id(id):
                    # Case 2: Single id provided, list accession for that crop
                    group = Group.objects(id=id).first()
                    if group is None:
                        return jsonify({"error": "Group not found"}), 404
                    accessions = Accession.objects(landrace_group=group)
                    json_data = [{"id": str(x.id), "species_name": x.species_name,
                                "ext_id": x.ext_id, "crop": str(x.crop.id),
                                "landrace_group":str(x.landrace_group.id), 
                                "institution_name":x.institution_name,
                                "source_database":x.source_database,
                                "latitude":x.latitude,
                                "longitude":x.longitude,
                                "accession_id":x.accession_id}
                                for x in accessions]
                    return json_data
                else:
                    return {'message': 'Invalid crop ID'}, 400
            else:
                # Case 3: List of ids provided, list accession for each crop separately
                json_data = []
                for group_id in id_list:     
                    if is_valid_object_id(group_id):
                        group = Group.objects(id=group_id).first()
                        if group is None:
                            json_data.append({"error": f"Group with id {group_id} not found"})
                        else:
                            accessions = Accession.objects(landrace_group=group)
                            group_data = {"group_id": str(group.id),
                                        "accessions": [{"id": str(x.id), "species_name": x.species_name,
                                                        "ext_id": x.ext_id, "crop": str(x.crop.id),
                                                        "landrace_group":str(x.landrace_group.id), 
                                                        "institution_name":x.institution_name,
                                                        "source_database":x.source_database,
                                                        "latitude":x.latitude,
                                                        "longitude":x.longitude,
                                                        "accession_id":x.accession_id}
                                                        for x in accessions]}
                            json_data.append(group_data)
                    else:
                        json_data.append({"crop_id": group_id,"error": "Invalid group ID"})
                return json_data
        else: 
            return {'message': 'Invalid group ID'}, 400