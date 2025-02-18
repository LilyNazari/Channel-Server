
#__________________________________________IMPORTS
from flask import Flask, request, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
import json 
import datetime 
import requests   
from flask_user import UserManager, UserMixin
from flask_cors import CORS

db = SQLAlchemy() 
#__________________________________________DATA MODEL:Defining the Channel model representing the channels table in the database
################ NB: Make sure to add flask_user UserMixin as this adds additional fields and properties required by Flask-User
class Channel(db.Model):
    __tablename__ = 'channels'
    id = db.Column(db.Integer, primary_key=True)
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')
    name = db.Column(db.String(100, collation='NOCASE'), nullable=False)
    endpoint = db.Column(db.String(100, collation='NOCASE'), nullable=False, unique=True)
    authkey = db.Column(db.String(100, collation='NOCASE'), nullable=False)
    type_of_service = db.Column(db.String(100, collation='NOCASE'), nullable=False)
    last_heartbeat = db.Column(db.DateTime(), nullable=True, server_default=None)


#__________________________________________USER MODEL required by Flask-User for authentication and account management
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100, collation='NOCASE'), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean(), nullable=False, server_default='1')
    email_confirmed_at = db.Column(db.DateTime())


#__________________________________________Class-Based Configuration for the Flask Application
class ConfigClass(object):
    ########################### Secret key for session management (Note: Replace this in production)

    # Flask settings
    SECRET_KEY = 'This is an INSECURE secret!! DO NOT use this in production!!'
    # Flask-SQLAlchemy settings
    SQLALCHEMY_DATABASE_URI = 'sqlite:///chat_server.sqlite'  
    SQLALCHEMY_TRACK_MODIFICATIONS = False  
    # Flask-User settings
    USER_MANAGER_ENABLE_EMAIL = False  # Disabled email for now
    USER_APP_NAME = "Chat Server"  # Shown in emails and page titles
    USER_ENABLE_USERNAME = True  
    USER_REQUIRE_RETYPE_PASSWORD = False  # Disabled password for now
    USER_EMAIL_SENDER_EMAIL = "noreply@example.com"


#__________________________________________APP INITIALIZATION: Creation & Configuration of an instance of the Flask application
app = Flask(__name__, static_folder="../Front3/build/static")
app.config.from_object(__name__ + '.ConfigClass')  # 
app.app_context().push() 
db.init_app(app)  
db.create_all()  
user_manager = UserManager(app, db, User) # Setting up Flask-User to handle user authentication and account management
SERVER_AUTHKEY = '1234567890'  # Server authorization key used for validating incoming requests
CORS(app, origins="http://localhost:3000")
#__________________________________________ROUTES: Home page route - Displaying a list of all channels and is accessible to anyone
@app.route('/')
def home_page():
    channels = Channel.query.all()      # Query all channels from the database
    return render_template("home.html", channels=channels)      # Render the home.html template, passing the channels list to the template


#__________________________________________ HELPER FUNCTIONS to perform health check for a given channel
def health_check(endpoint, authkey):
    response = requests.get(endpoint+'/health', # Make a GET request to the channel's health endpoint 
                            headers={'Authorization': 'authkey '+authkey})
    if response.status_code != 200: # Check if the response status is 200 (OK) or the health check is failed.
        return False
    if 'name' not in response.json(): # Check if the response is JSON and contains the channel name
        return False
    channel = Channel.query.filter_by(endpoint=endpoint).first()      # Check if the channel name matches the expected name in the database
    if not channel:
        print(f"Channel {endpoint} not found in database")
        return False
    expected_name = channel.name      
    if response.json()['name'] != expected_name:
        return False

    channel.last_heartbeat = datetime.datetime.now()      # If all checks pass, update the last_heartbeat to the current time
    db.session.commit()    # Commit the update to the database
    return True      # Return True indicating the channel passed the health check


#__________________________________________REST API ENDPOINTS: Flask REST route endpoints for creating or updating a channel (POST request)
@app.route('/channels', methods=['POST'])
def create_channel():
    global SERVER_AUTHKEY
    record = json.loads(request.data)
    if 'Authorization' not in request.headers:  #Authorization check
        return "No authorization header", 400
    if request.headers['Authorization'] != 'authkey ' + SERVER_AUTHKEY:
        return "Invalid authorization header ({})".format(request.headers['Authorization']), 400
    if 'name' not in record:     
        return "Record has no name", 400
    if 'endpoint' not in record:
        return "Record has no endpoint", 400
    if 'authkey' not in record:
        return "Record has no authkey", 400
    if 'type_of_service' not in record:
        return "Record has no type of service representation", 400
    update_channel = Channel.query.filter_by(endpoint=record['endpoint']).first()
    print("update_channel: ", update_channel)
    if update_channel:  # If channel already exists, update it
        update_channel.name = record['name']
        update_channel.authkey = record['authkey']
        update_channel.type_of_service = record['type_of_service']
        update_channel.active = False
        db.session.commit()         # Save changes to the database
        if not health_check(record['endpoint'], record['authkey']):     # Perform health check to validate channel status
            return "Channel is not healthy", 400
        return jsonify(created=False,          
                       id=update_channel.id), 200
    else:  # If channel does not exist, create a new one
        channel = Channel(name=record['name'],
                          endpoint=record['endpoint'],
                          authkey=record['authkey'],
                          type_of_service=record['type_of_service'],
                          last_heartbeat=datetime.datetime.now(),
                          active=True)
        db.session.add(channel)          # Add and commit the new channel to the database
        db.session.commit() 
        if not health_check(record['endpoint'], record['authkey']):          # Perform health check & if health check fails, delete the newly created channel
            db.session.delete(channel)  # delete channel from database
            db.session.commit()
            return "Channel is not healthy", 400         # Return JSON response indicating creation
        return jsonify(created=True, id=channel.id), 200

# Endpoint for retrieving all channels (GET request)

@app.route('/channels', methods=['GET'])
def get_channels():
    channels = Channel.query.all()     # Query all channels from the database
    return jsonify(channels=[{'name': c.name,         # Return JSON response containing all channels' data
                              'endpoint': c.endpoint,
                              'authkey': c.authkey,
                              'type_of_service': c.type_of_service} for c in channels]), 200

#__________________________________________________________________APPLICATION ENTRY POINT: Run the Flask application on port 5555 in debug mode
if __name__ == '__main__':
    app.run(port=5555, debug=True)
