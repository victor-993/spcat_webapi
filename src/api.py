
from flask import Flask, redirect, send_from_directory
from flask_restful import Api
from flask_cors import CORS
from mongoengine import connect
from config import config
from flask_swagger_ui import get_swaggerui_blueprint

from modules.country import Countries
from modules.crops import Crops, Groups, GroupsByIDCrop
from modules.accessions import AccessionsByIDCrop, AccessionsByIDGroup

app = Flask(__name__)
CORS(app)
api = Api(app)

SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': "Gap Analysis Web API"}
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)

@app.route('/')
def home():
    return redirect("/swagger")

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static',path)

api.add_resource(Countries, '/countries')
api.add_resource(Crops, '/crops')
api.add_resource(Groups, '/groups')
api.add_resource(GroupsByIDCrop, '/groupsbyids' , '/groupsbyids/<string:id>')
api.add_resource(AccessionsByIDCrop, '/accessionsbyidcrop', '/accessionsbyidcrop/<string:id>')
api.add_resource(AccessionsByIDGroup, '/accessionsbyidgroup', '/accessionsbyidgroup/<string:id>')



if __name__ == '__main__':
    connect(host=config['CONNECTION_DB'])
    print("Connected DB")
    
    if config['DEBUG']:
        app.run(threaded=True, port=config['PORT'], debug=config['DEBUG'])
    else:
        app.run(host=config['HOST'], port=config['PORT'],
                debug=config['DEBUG'])
