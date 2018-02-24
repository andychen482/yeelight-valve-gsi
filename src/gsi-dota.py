from http.server import BaseHTTPRequestHandler, HTTPServer
from yeelight import Bulb
import sys
import time
import json
import configparser

class MyServer(HTTPServer):
    def init_state(self):
        self.health = None

class MyRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers['Content-Length'])
        body = self.rfile.read(length).decode('utf-8')
        self.parse_payload(json.loads(body))
        self.send_header('Content-type', 'text/html')
        self.send_response(200)
        self.end_headers()

    def parse_payload(self, payload):
        health = self.get_health(payload)
        if health != self.server.health:
            self.server.health = health
            print('health state changed to %s' % health)
            for bulbn in (bulb1, bulb2, bulb3):
                if bulbn != '':
                    bulb = Bulb(bulbn)
                    if health <= 50:
                        bulb.set_rgb(255, 255, 0)
                    if health <= 20:
                        bulb.set_rgb(255, 51, 0)
                    if health <= 10:
                        bulb.set_rgb(255, 0, 0)

    def get_health(self, payload):
        if 'hero' in payload and 'health_percent' in payload['hero']:
            return payload['hero']['health_percent']
        else:
            return None
    
    def log_message(self, format, *args):
        return

print('Initializing yeelight-gsi by davidramiro')
server = MyServer(('localhost', 3000), MyRequestHandler)
server.init_state()
print('Reading config...')
config = configparser.ConfigParser()
config.read('config.ini')
bulb1 = config.get('lamps','ip1')
bulb2 = config.get('lamps','ip2')
bulb3 = config.get('lamps','ip3')
for bulbn in (bulb1, bulb2, bulb3):
    if bulbn != '':
        print('Initializing Yeelight at %s' % bulbn)
        bulb = Bulb(bulbn)
        bulb.turn_on()
        bulb.start_music()
        bulb.set_rgb(0, 0, 255)
        bulb.set_brightness(100)

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
print(time.asctime(), '-', 'yeelight-gsi is running')
