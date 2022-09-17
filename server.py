from flask import Flask, request
import json

class Server:
    def __init__(self):
        self.players = {}
    def position(self):return json.dumps(self.players)



    def add_position(self):
        try:
            req_json=json.loads(request.json)
            self.players[req_json.get('uid')]=req_json.get('position')
            return json.dumps(self.players)
        except:
            return 'ERROR'



host="192.168.0.108"
port="4567"

app = Flask(__name__)
server = Server()

@app.route("/player-position")
def call1():return server.position()
@app.route("/post-position",  methods=["post"])
def call2():return server.add_position()

#app.run(debug=True, port=port, host=host)
