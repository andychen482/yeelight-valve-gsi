from http.server import BaseHTTPRequestHandler, HTTPServer
from yeelight import *
import sys
import time
import json
import configparser

flashFlow = [
    RGBTransition(255, 0, 0, duration=100, brightness=100),
    RGBTransition(255, 153, 0, duration=100, brightness=100),
]
bulbs = []


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
            if 100 >= health > 50:
                changeLight(0, 255, 0)
            if health <= 50:
                changeLight(255, 255, 0)
            if health <= 20:
                changeLight(255, 51, 0)
            if health <= 10:
                changeLight(255, 0, 0)
                flash()

    def get_health(self, payload):
        if 'hero' in payload and 'health_percent' in payload['hero']:
            return payload['hero']['health_percent']
        else:
            return None

    def log_message(self, format, *args):
        return


def flash():
    for bulbn in bulbs:
        if bulbn != '':
            bulb = Bulb(bulbn)
            bulb.start_flow(Flow(3, Flow.actions.recover, flashFlow))


def changeLight(r, g, b):
    for bulbn in bulbs:
        if bulbn != '':
            bulb = Bulb(bulbn)
            bulb.set_rgb(r, g, b)


def main():
    print('Welcome to yeelight-gsi by davidramiro')
    print('Reading config...')
    config = configparser.ConfigParser()
    config.read('config.ini')
    bulb_count = int(config.get('general', 'Lamp Count'))
    for n in range(1, (bulb_count + 1)):
        bulbs.append(config.get(str(n), 'ip'))
    print('Initializing...')
    server = MyServer(('localhost', 3000), MyRequestHandler)
    server.init_state()
    for bulbn in bulbs:
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
    for bulbn in bulbs:
        if bulbn != '':
            bulb = Bulb(bulbn)
            bulb.stop_music
    print(time.asctime(), '-', 'Listener stopped. Thanks for using yeelight-gsi!')


main()
