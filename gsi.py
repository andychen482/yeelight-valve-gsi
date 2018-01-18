from http.server import BaseHTTPRequestHandler, HTTPServer
from yeelight import Bulb
import sys
import time
import json


class MyServer(HTTPServer):
    def init_state(self):
        self.round_phase = None
        self.round_bomb = None
        self.player_state = None
        self.player_health = None

class MyRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers['Content-Length'])
        body = self.rfile.read(length).decode('utf-8')

        self.parse_payload(json.loads(body))

        self.send_header('Content-type', 'text/html')
        self.send_response(200)
        self.end_headers()

    def parse_payload(self, payload):
        round_phase = self.get_round_phase(payload)
        round_bomb = self.get_round_bomb(payload)
        player_state = self.get_player_state(payload)
        player_health = self.get_player_health(payload)
        
        if round_phase != self.server.round_phase:
            self.server.round_phase = round_phase
            print('round phase: %s' % round_phase)
            
            if 'over' in round_phase:
                bulb.set_rgb(255, 0, 0)
        
            if 'live' in round_phase:
                bulb.set_rgb(153, 102, 255)
            
            if 'freezetime' in round_phase:
                bulb.set_rgb(0, 0, 255)
        
    def get_round_phase(self, payload):
        if 'round' in payload and 'phase' in payload['round']:
            return payload['round']['phase']
        else:
            return None
            
    def get_round_bomb(self, payload):
        if 'round' in payload and 'bomb' in payload['round']:
            return payload['round']['bomb']
        else:
            return None
            
    def get_player_state(self, payload):
        if 'player' in payload and 'state' in payload['player']:
            return payload['player']['state']
            print('new payload player & state')
        else:
            return None
            
    def get_player_health(self, payload):
        if 'health' in payload:
            return payload['health']
            print('new payload player & state')
        else:
            return None

    def log_message(self, format, *args):
        return

server = MyServer(('localhost', 3000), MyRequestHandler)
server.init_state()

address = input("Enter the lamp's IP address: ")
print('Initializing Yeelight')

bulb = Bulb(address)
bulb.turn_on()
bulb.start_music()
bulb.set_rgb(0, 0, 255)
bulb.set_brightness(100)

print(time.asctime(), '-', 'GSI running')

try:
    server.serve_forever()
except (KeyboardInterrupt, SystemExit):
    pass

server.server_close()
bulb.stop_music
print(time.asctime(), '-', 'GSI server stopped')
