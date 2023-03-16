from flask import Flask, jsonify
from flask_restful import Resource
from ormgap import Country

class Countries(Resource):

    def __init__(self):
        super().__init__()

    def get(self):
        """
        Get all countries from database
        ---
        responses:
          200:
            description: 
            schema:
              id: Country
              properties:
                id:
                  type: string
                  description: Id Country
                name:
                  type: string
                  description: Country name
                ext_id:
                  type: string
                  description: ISO 2 code (ISO 3166-1 alpha-2) to identify Country
        """
        q_set = None
        q_set = Country.objects()
        json_data = [{"id":str(x.id),"name":x.name,"iso_2":x.iso_2} for x in q_set]
        return json_data
