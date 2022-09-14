from flask import Flask, render_template, url_for, request, redirect, abort, make_response, session, send_from_directory
import json
from threading import Thread
import time


ip="192.168.0.108"
host = "http://192.168.0.108:4567/"
port="4567"
app = Flask(__name__)


@app.route("/player-position")
def position():
    with open(f'game.json','r') as file:
        json_ = json.load(file)
    return json_


@app.route("/post-position",  methods=["post"])
def add_position():
    req_json=json.loads(request.json)
    with open('game.json','r') as file:
        json_ = json.load(file)
    try:json_['players'][req_json.get('uid')]=req_json.get('position')
    except:pass
    with open('game.json','w') as file:
        json.dump(json_, file)
    return json_

@app.route("/post-message",  methods=["post"])
def add_message():
    req_json=json.loads(request.json)
    with open('game.json','r') as file:
        json_ = json.load(file)
    try:json_['messages'][req_json.get('uid')]=req_json.get('message')
    except:pass
    with open('game.json','w') as file:
        json.dump(json_, file)
    return json_

#app.run(debug=True, port=port, host=ip)
