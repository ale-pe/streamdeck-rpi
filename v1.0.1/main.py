from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, send,join_room, leave_room
import math,random
import json
###OBS###
import sys
import time
import logging
logging.basicConfig(level=logging.INFO)

sys.path.append('../')
from obswebsocket import obsws, requests  # noqa: E402


host = "localhost"
port = 4444
password = "123123"

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
    return render_template('deck.html')

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



@socketio.on('changescenes')
def test_connectb(data):
        d1 = data
        s1 = json.dumps(d1)
        d2 = json.loads(s1)
        print(d2["scene"])
        ws.call(requests.SetCurrentScene(d2["scene"]))


if __name__ == '__main__':
    socketio.run(app, debug=True, host="192.168.1.15" , port=5001)