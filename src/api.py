
from flask import Flask, redirect
from flask_restful import Api
from flask_cors import CORS
from mongoengine import connect
from config import config

from modules.country import Countries
from modules.crops import Crops, Groups, GroupsByIDCrop
from modules.accessions import AccessionsByIDCrop, AccessionsByIDGroup

app = Flask(__name__)
CORS(app)
api = Api(app)

api.add_resource(Countries, '/countries')
api.add_resource(Crops, '/crops')
api.add_resource(Groups, '/groups')
api.add_resource(GroupsByIDCrop, '/groupsbyids' , '/groupsbyid2/<string:id>')
api.add_resource(AccessionsByIDCrop, '/accessionsbyidcrop' , '/accessionsbyidcrop/<string:id>')
api.add_resource(AccessionsByIDGroup, '/accessionsbyidgroup' , '/accessionsbyidgroup/<string:id>')



if __name__ == '__main__':
    connect(host=config['CONNECTION_DB'])
    print("Connected DB")
    
    if config['DEBUG']:
        app.run(threaded=True, port=config['PORT'], debug=config['DEBUG'])
    else:
        app.run(host=config['HOST'], port=config['PORT'],
                debug=config['DEBUG'])
