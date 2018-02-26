from http.server import BaseHTTPRequestHandler, HTTPServer
from yeelight import *
import sys
import time
import json
import configparser

alarmFlow = [
    HSVTransition(0, 100, duration=250, brightness=100),
    HSVTransition(0, 100, duration=250, brightness=60),
]
bombFlow = [
    RGBTransition(255, 0, 0, duration=900, brightness=100),
    RGBTransition(255, 153, 0, duration=100, brightness=100),
]

class MyServer(HTTPServer):
    def init_state(self):
        self.round_phase = None
        self.round_bomb = None
        self.player_health = None
        self.weapon_ammo = None

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
        weapon_ammo = self.get_weapon_ammo(payload)

        if round_bomb != self.server.round_bomb:
            self.server.round_bomb = round_bomb
            print('changed bomb status: %s' % round_bomb)
            if 'planted' in round_bomb:
                police()
            if 'defused' in round_bomb:
                changeLight(0, 0, 255)

        if round_phase != self.server.round_phase:
            self.server.round_phase = round_phase
            print('new round phase: %s' % round_phase)
            if 'over' in round_phase:
                changeLight(255, 0, 0)
            if 'live' in round_phase:
                changeLight(153, 102, 255)
            if 'freezetime' in round_phase:
                changeLight(0, 0, 255)

        if player_health != self.server.player_health:
            self.server.player_health = player_health
            print('player health: %s' % player_health)
            if player_health <= 50:
                changeLight(255, 255, 0)
            if player_health <= 20:
                changeLight(255, 51, 0)
            if player_health <= 10:
               alarm()
        
        if weapon_ammo != self.server.weapon_ammo:
            self.server.weapon_ammo = weapon_ammo
            print('weapon ammo: %s' % weapon_ammo)
            if player_health <= 5:
                changeLight(255, 255, 255)

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
        if useHealth == True:
            if 'player' in payload and 'state' in payload['player']:
                return payload['player']['state']['health']
            else:
                return None
                
    def get_weapon_ammo(self, payload):
        if useAmmo == True:
            if 'player_weapons' in payload:
                return payload['player_weapons']['player']['weapons']['weapon_3']['ammo_clip']
            else:
                return None

    def log_message(self, format, *args):
        return

def changeLight(r, g, b):
    for bulbn in (bulb1, bulb2, bulb3):
        if bulbn != '':
            bulb = Bulb(bulbn)
            bulb.set_rgb(r, g, b)
            
def alarm():
    for bulbn in (bulb1, bulb2, bulb3):
        if bulbn != '':
            bulb = Bulb(bulbn)
            bulb.start_flow(Flow(2, Flow.actions.recover, alarmFlow))

def police():
    for bulbn in (bulb1, bulb2, bulb3):
        if bulbn != '':
            bulb = Bulb(bulbn)
            bulb.start_flow(Flow(40, Flow.actions.recover, bombFlow))

def readConfig():
    print('Reading config...')
    config = configparser.ConfigParser()
    config.read('config.ini')
    global bulb1,bulb2,bulb3,usePhase,useBomb,useHealth,useAmmo
    bulb1 = config.get('lamps','ip1')
    bulb2 = config.get('lamps','ip2')
    bulb3 = config.get('lamps','ip3')
    usePhase = config.getboolean('csgo settings','round phase colors')
    useBomb = config.getboolean('csgo settings','c4 status colors')
    useHealth = config.getboolean('csgo settings','health colors')
    useAmmo = config.getboolean('csgo settings','ammo colors')            
            
def main():
    print('Welcome to yeelight-gsi by davidramiro')
    readConfig()
    print('Initializing...')
    for bulbn in (bulb1, bulb2, bulb3):
        if bulbn != '':
            print('Initializing Yeelight at %s' % bulbn)
            bulb = Bulb(bulbn)
            bulb.turn_on()
            bulb.start_music()
            bulb.set_rgb(0, 0, 255)
            bulb.set_brightness(100)
    server = MyServer(('localhost', 3000), MyRequestHandler)
    server.init_state()
    print(time.asctime(), '-', 'yeelight-gsi is running - CTRL+C to stop')
    try:
        server.serve_forever()
    except (KeyboardInterrupt, SystemExit):
        pass
    server.server_close()
    for bulbn in (bulb1, bulb2, bulb3):
        if bulbn != '':
            bulb = Bulb(bulbn)
            bulb.stop_music
            bulb.set_rgb(255,255,255)
            bulb.set_brightness(100)
    print(time.asctime(), '-', 'Listener stopped. Thanks for using yeelight-gsi!')
    
main()