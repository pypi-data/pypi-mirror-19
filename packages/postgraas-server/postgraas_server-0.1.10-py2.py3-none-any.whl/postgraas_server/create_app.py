from flask import Flask
from flask_restful import fields, Resource, marshal_with, Api, reqparse
from postgraas_server.management_resources import db
from postgraas_server.management_resources import DBInstanceResource, DBInstanceCollectionResource
from postgraas_server.configuration import get_meta_db_config_path


def create_app(config):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = get_meta_db_config_path(config)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    restful_api = Api(app)
    restful_api.add_resource(DBInstanceResource, "/api/v2/postgraas_instances/<int:id>")
    restful_api.add_resource(DBInstanceCollectionResource, "/api/v2/postgraas_instances")
    db.init_app(app)
    return app