from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flask_migrate import Migrate
from models import db
from config import config

# Import routes
from routes.ngos import NGOListResource, NGOResource
from routes.tasks import TaskListResource, TaskResource
from routes.signups import SignupListResource, SignupResource

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    migrate = Migrate(app, db)
    CORS(app)
    
    # Create API and register routes (same as before)
    api = Api(app)
    api.add_resource(NGOListResource, '/api/ngos')
    # ... rest of your route registrations
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)