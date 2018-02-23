from http.server import BaseHTTPRequestHandler, HTTPServer
from yeelight import Bulb
import sys
import time
import json
import configparser


class MyServer(HTTPServer):
    def init_state(self):
        self.round_phase = None
        self.round_bomb = None
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
        player_health = self.get_player_health(payload)

        if round_bomb != self.server.round_bomb:
            self.server.round_bomb = round_bomb
            print('changed bomb status: %s' % round_bomb)
            if 'exploded' in round_bomb:
                if bulb1 != '':
                    bulb = Bulb(bulb1)
                    bulb.set_rgb(0, 255, 0)
                if bulb2 != '':
                    bulb = Bulb(bulb2)
                    bulb.set_rgb(0, 255, 0)
                if bulb3 != '':
                    bulb = Bulb(bulb3)
                    bulb.set_rgb(0, 255, 0)
            if 'planted' in round_bomb:
                if bulb1 != '':
                    bulb = Bulb(bulb1)
                    bulb.set_rgb(255, 0, 0)
                if bulb2 != '':
                    bulb = Bulb(bulb2)
                    bulb.set_rgb(255, 0, 0)
                if bulb3 != '':
                    bulb = Bulb(bulb3)
                    bulb.set_rgb(255, 0, 0)
            if 'defused' in round_bomb:
                if bulb1 != '':
                    bulb = Bulb(bulb1)
                    bulb.set_rgb(0, 0, 255)
                if bulb2 != '':
                    bulb = Bulb(bulb2)
                    bulb.set_rgb(0, 0, 255)
                if bulb3 != '':
                    bulb = Bulb(bulb3)
                    bulb.set_rgb(0, 0, 255)

        if round_phase != self.server.round_phase:
            self.server.round_phase = round_phase
            print('new round phase: %s' % round_phase)
            if 'over' in round_phase:
                if bulb1 != '':
                    bulb = Bulb(bulb1)
                    bulb.set_rgb(255, 0, 0)
                if bulb2 != '':
                    bulb = Bulb(bulb2)
                    bulb.set_rgb(255, 0, 0)
                if bulb3 != '':
                    bulb = Bulb(bulb3)
                    bulb.set_rgb(255, 0, 0)
            if 'live' in round_phase:
                if bulb1 != '':
                    bulb = Bulb(bulb1)
                    bulb.set_rgb(153, 102, 255)
                if bulb2 != '':
                    bulb = Bulb(bulb2)
                    bulb.set_rgb(153, 102, 255)
                if bulb3bulb3 != '':
                    bulb = Bulb(bulb3)
                    bulb.set_rgb(153, 102, 255)
            if 'freezetime' in round_phase:
                if bulb1 != '':
                    bulb = Bulb(bulb1)
                    bulb.set_rgb(0, 0, 255)
                if bulb2 != '':
                    bulb = Bulb(bulb2)
                    bulb.set_rgb(0, 0, 255)
                if bulb3 != '':
                    bulb = Bulb(bulb3)
                    bulb.set_rgb(0, 0, 255)

        if player_health != self.server.player_health:
            self.server.player_health = player_health
            print('player health: %s' % player_health)
            if bulb1 != '':
                bulb = Bulb(bulb1)
                bulb.set_rgb(0xff0000 * player_health)
            if bulb2 != '':
                bulb = Bulb(bulb2)
                bulb.set_rgb(0xff0000 * player_health)
            if bulb3 != '':
                bulb = Bulb(bulb3)
                bulb.set_rgb(0xff0000 * player_health)

    def get_round_phase(self, payload):
        if usePhase == True:
            if 'round' in payload and 'phase' in payload['round']:
                return payload['round']['phase']
            else:
                return None

    def get_round_bomb(self, payload):
        if useBomb == True:
            if 'round' in payload and 'bomb' in payload['round']:
                return payload['round']['bomb']
            else:
                return None

    def get_player_health(self, payload):
        if 'player' in payload and 'state' in payload['player']:
            return payload['player']['state']['health']
        else:
            return None

    def log_message(self, format, *args):
        return

server = MyServer(('localhost', 3000), MyRequestHandler)
server.init_state()

config = configparser.ConfigParser()
config.read('config.ini')
bulb1 = config.get('lamps','ip1')
bulb2 = config.get('lamps','ip2')
bulb3 = config.get('lamps','ip3')
usePhase = config.getboolean('csgo settings','round phase colors')
useBomb = config.getboolean('csgo settings','c4 status colors')
useHealth = config.getboolean('csgo settings','health colors')

if bulb1 != '':
    print('Initializing first Yeelight')
    bulb = Bulb(bulb1)
    bulb.turn_on()
    bulb.start_music()
    bulb.set_rgb(0, 0, 255)
    bulb.set_brightness(100)

if bulb2 != '':
    print('Initializing second Yeelight')
    bulb = Bulb(bulb2)
    bulb.turn_on()
    bulb.start_music()
    bulb.set_rgb(0, 0, 255)
    bulb.set_brightness(100)

if bulb3 != '':
    print('Initializing third Yeelight')
    bulb = Bulb(bulb3)
    bulb.turn_on()
    bulb.start_music()
    bulb.set_rgb(0, 0, 255)
    bulb.set_brightness(100)

print(time.asctime(), '-', 'GSI running - CTRL+C to stop')
try:
    server.serve_forever()
except (KeyboardInterrupt, SystemExit):
    pass

server.server_close()

if bulb1 != '':
    bulb = Bulb(bulb1)
    bulb.stop_music
if bulb2 != '':
    bulb = Bulb(bulb2)
    bulb.stop_music
if bulb3 != '':
    bulb = Bulb(bulb3)
    bulb.stop_music

print(time.asctime(), '-', 'GSI server stopped')
