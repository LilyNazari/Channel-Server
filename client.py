#__________________________________________IMPORTS
from flask import Flask, request, render_template, url_for, redirect
import requests
import urllib.parse
import datetime
from flask_cors import CORS
import os
from flask import send_from_directory
#______________________________________Flask Application Initialization
app = Flask(__name__, static_folder="../Front3/build/static")
#______________________________________React App Routing To Main Page
@app.route('/')
def serve_react_app(): # Send index.html from React build folder
    return send_from_directory(os.path.join(app.root_path, '../Front3/build'), 'index.html')
@app.route('/static/<path:path>') # Serve static files (CSS, JS, images) from the React app
def serve_static(path):
    return send_from_directory(os.path.join(app.root_path, '../Front3/build/static'), path)
#______________________________________Server Configuration
HUB_AUTHKEY = '1234567890'# Authentication key for Hub
HUB_URL = 'http://localhost:5555'# Hub endpoint URL
CHANNELS = None# Cached list of channels
LAST_CHANNEL_UPDATE = None# Timestamp of last channel update
#______________________________________CORS Configuration: Allowing React app to make requests
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})
#______________________________________Channel Validation Update
def update_channels():
    global CHANNELS, LAST_CHANNEL_UPDATE
    if CHANNELS and LAST_CHANNEL_UPDATE and (datetime.datetime.now() - LAST_CHANNEL_UPDATE).seconds < 60:
        return CHANNELS # fetch list of channels from server
    response = requests.get(HUB_URL + '/channels', headers={'Authorization': 'authkey ' + HUB_AUTHKEY})
    if response.status_code != 200:
        return "Error fetching channels: "+str(response.text), 400
    channels_response = response.json()
    if not 'channels' in channels_response:
        return "No channels in response", 400
    CHANNELS = channels_response['channels']
    LAST_CHANNEL_UPDATE = datetime.datetime.now()
    return CHANNELS
#______________________________________Routing To Home Page to fetch list of channels from server
@app.route('/home')
def home_page():    
    return render_template("home.html", channels=update_channels())

#______________________________________Routing To Show and display list of messages from channel
@app.route('/show')
def show_channel():
    show_channel = request.args.get('channel', None)
    if not show_channel:
        return "No channel specified", 400
    channel = None
    for c in update_channels():
        if c['endpoint'] == urllib.parse.unquote(show_channel):
            channel = c
            break
    if not channel:
        return "Channel not found", 404
    response = requests.get(channel['endpoint'], headers={'Authorization': 'authkey ' + channel['authkey']})
    if response.status_code != 200:
        return "Error fetching messages: "+str(response.text), 400
    messages = response.json()
    return render_template("channel.html", channel=channel, messages=messages)

#______________________________________Routing To Send A Message To The Channel
@app.route('/post', methods=['POST'])
def post_message():
    post_channel = request.form['channel']
    if not post_channel:
        return "No channel specified", 400
    channel = None
    for c in update_channels():
        if c['endpoint'] == urllib.parse.unquote(post_channel):
            channel = c
            break
    if not channel:
        return "Channel not found", 404
    message_content = request.form['content']
    message_sender = request.form['sender']
    message_timestamp = datetime.datetime.now().isoformat()
    response = requests.post(channel['endpoint'],
                             headers={'Authorization': 'authkey ' + channel['authkey']},
                             json={'content': message_content, 'sender': message_sender, 'timestamp': message_timestamp})
    if response.status_code != 200:
        return "Error posting message: "+str(response.text), 400
    return redirect(url_for('show_channel')+'?channel='+urllib.parse.quote(post_channel))
#______________________________________Application Entry Point
if __name__ == '__main__':
    app.run(port=5005, debug=True)# Start development server on port 5005
