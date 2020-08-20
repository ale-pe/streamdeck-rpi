from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, send,join_room, leave_room
import math,random
import json
import configparser
import os

###OBS###
import sys
import time
import logging
logging.basicConfig(level=logging.INFO)

sys.path.append('../')
from obswebsocket import obsws, requests  # noqa: E402
config = configparser.ConfigParser()
config.read('file.ini')

host = config['parametre-obs']['adresse']
port = config['parametre-obs']['port']
password = config['parametre-obs']['mot-de-passe']

ws = obsws(host, port, password)
ws.connect()
######

# initialize Flask
app = Flask(__name__)
socketio = SocketIO(app)
ROOMS = {} # dict to track active rooms


@app.route('/deck')
def player():
    """Serve the index HTML"""
    return render_template('TEST1.html')

@app.route('/scenes')
def player2():
    """Serve the index HTML"""
    return render_template('scenes.html')

@socketio.on('datalive')
def test_connect():

    stream = ws.call(requests.GetStreamingStatus())
#     print(stream.getRecording())
    vol = ws.call(requests.GetSourcesList())
    print(vol)
    emit('data', {'livestate': stream.getStreaming(),'recordstate': stream.getRecording()})

@socketio.on('rec')
def test_connect():
    ws.call(requests.StartStopRecording())
    stream = ws.call(requests.GetStreamingStatus())
    emit('data', {'livestate': stream.getStreaming(),'recordstate': stream.getRecording()})

@socketio.on('live')
def test_connect():
    ws.call(requests.StartStopStreaming())
    stream = ws.call(requests.GetStreamingStatus())
    emit('data', {'livestate': stream.getStreaming(),'recordstate': stream.getRecording()})
    
@socketio.on('getscenes')
def test_connecta():
    scenes = ws.call(requests.GetSceneList())
    for s in scenes.getScenes():
        name = s['name']
        emit('getscenes',{'name': name})

@socketio.on('twitchopen')
def test_connectc():
    os.system('cmd /c "start https://twitch.tv/"'+config['twitch']['pseudo_twitch']) 

@socketio.on('spotifyopen')
def test_connectc():
    os.system('cmd /c "start spotify"') 


@socketio.on('changescenes')
def test_connectb(data):
        d1 = data
        s1 = json.dumps(d1)
        d2 = json.loads(s1)
        print(d2["scene"])
        ws.call(requests.SetCurrentScene(d2["scene"]))
        print("ok")

if __name__ == '__main__':
    host = config['pc']['adresse-locale-du-pc']
    port =  config['pc']['port-pour-le-serveur']
    socketio.run(app, debug=True, host=host , port=int(port))