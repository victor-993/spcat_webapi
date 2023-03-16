from flask import Flask, jsonify, request
from flask_restful import Resource
from ormgap import Crop, Group
import re
import json
import ast

def is_valid_object_id(value):
    """
    Returns True if `value` is a valid hexadecimal string representation of an ObjectId, False otherwise.
    """
    if not isinstance(value, str):
        return False
    pattern = re.compile("[0-9a-f]{24}")
    return pattern.match(value) is not None

class Crops(Resource):

    def __init__(self):
        super().__init__()

    def get(self):
        """
        Get all crops from database
        ---
        responses:
          200:
            description: 
            schema:
              id: Crop
              properties:
                id:
                  type: string
                  description: Id crop
                name:
                  type: string
                  description: Crop name
                ext_id:
                  type: string
                  description: Extern Id to identify crop
                base_name: 
                  type: string
                  description: Base name of the crop.
                app_name: 
                  type: string
                  description: Application name of the crop.
        """
        q_set = None
        q_set = Crop.objects()
        json_data = [{"id":str(x.id),"name":x.name,"ext_id":x.ext_id, "base_name":x.base_name, "app_name":x.app_name} for x in q_set]
        return json_data
    
class Groups(Resource):

    def __init__(self):
        super().__init__()

    def get(self):
        """
        Get all groups from database
        ---
        responses:
          200:
            description: 
            schema:
              id: Group
              properties:
                id:
                  type: string
                  description: Id group
                group_name:
                  type: string
                  description: Group name
                ext_id:
                  type: string
                  description: Extern Id to identify group
                crop: 
                  type: string
                  description: Id crop that the group belongs to.
        """
        q_set = None
        q_set = Group.objects()
        json_data = [{"id":str(x.id),"group_name":x.group_name,"ext_id":x.ext_id, "crop":str(x.crop.id)} for x in q_set]
        return json_data
    

class GroupsByIDCrop(Resource):

    def __init__(self):
        super().__init__()

    def get(self):
        """
        Get groups from database by crop id(s)
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
              id: Group
              properties:
                id:
                  type: string
                  description: Id group
                group_name:
                  type: string
                  description: Group name
                ext_id:
                  type: string
                  description: Extern Id to identify group
                crop: 
                  type: string
                  description: Id crop that the group belongs to.
        """
        q_set = None
        
        # If id is a list of ids, return groups for each crop
        id = request.args.get('id')

        if id is not None:
            
            #first the blanks are eliminated, the ids are separated by commas and finally the repeated ones are eliminated.
            id_list = list(set(id.replace(" ", "").split(',')))
            print(id_list)

            if len(id_list) == 1:
                if is_valid_object_id(id_list[0]):
                    # Single id provided, list groups for that crop
                    crop = Crop.objects(id=id_list[0]).first()
                    if crop is None:
                        return {"error": f"Crop with id {id_list[0]} not found"}, 404
                    groups = Group.objects(crop=crop)
                    json_data = [{"id": str(x.id), "group_name": x.group_name,
                                "ext_id": x.ext_id, "crop": str(x.crop.id)}
                                for x in groups]
                    return json_data
                else:
                    return {'message': 'Invalid crop ID'}, 400
            else:
                # List of ids provided, list groups for each crop separately
                json_data = []
                for crop_id in id_list:     
                    if is_valid_object_id(crop_id):
                        crop = Crop.objects(id=crop_id).first()
                        if crop is None:
                            json_data.append({"error": f"Crop with id {crop_id} not found"})
                        else:
                            groups = Group.objects(crop=crop)
                            crop_data = {"crop_id": str(crop.id),
                                        "groups": [{"id": str(x.id),
                                                    "group_name": x.group_name,
                                                    "ext_id": x.ext_id, "crop":str(x.crop.id)}
                                                    for x in groups]}
                            json_data.append(crop_data)
                    else:
                        json_data.append({"crop_id": crop_id,"error": "Invalid crop ID"})
                return json_data
        else:
            return {'message': 'No crop IDs provided'}, 400