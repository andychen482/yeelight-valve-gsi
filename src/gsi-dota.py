from http.server import BaseHTTPRequestHandler, HTTPServer
from yeelight import *
import sys
import time
import json
import configparser

critical_flash = [
    RGBTransition(255, 0, 0, duration=200, brightness=100),
    RGBTransition(255, 153, 0, duration=200, brightness=100),
]
warning_flash = [
    RGBTransition(255, 0, 0, duration=200, brightness=100),
    RGBTransition(0, 0, 255, duration=200, brightness=100),
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
        silenced = self.get_silenced(payload)
        stunned = self.get_stunned(payload)
        hexed = self.get_hexed(payload)
        if health != self.server.health:
            self.server.health = health
            print('health state changed to %s' % health)
            hp_g = int(round(health / 100 * 255))
            hp_r = int(round((255 * (1 - health / 100))))
            changeLight(hp_r, hp_g, 0)
            if warn_low is True:
                if health <= 15:
                    print('Critical Health!')
                    flash()
                    time.sleep(0.8)

    def get_health(self, payload):
        if 'hero' in payload and 'health_percent' in payload['hero']:
            return payload['hero']['health_percent']
        else:
            return None

    def get_silenced(self, payload):
        if warn_slcd is True:
            if 'hero' in payload and 'silenced' in payload['hero']:
                if payload['hero']['silenced'] == True:
                    warn()
                    print("Your hero is silenced!")
                    time.sleep(0.8)
                return payload['hero']['silenced']
            else:
                return None

    def get_stunned(self, payload):
        if warn_stun is True:
            if 'hero' in payload and 'stunned' in payload['hero']:
                if payload['hero']['stunned'] == True:
                    warn()
                    print("Your hero is stunned!")
                    time.sleep(0.8)
                return payload['hero']['stunned']
            else:
                return None

    def get_hexed(self, payload):
        if warn_hex is True:
            if 'hero' in payload and 'hexed' in payload['hero']:
                if payload['hero']['hexed'] == True:
                    warn()
                    print("Your hero is hexed!")
                    time.sleep(0.8)
                return payload['hero']['hexed']
            else:
                return None

    def log_message(self, format, *args):
        return


def flash():
    for bulbn in bulbs:
        if bulbn != '':
            bulb = Bulb(bulbn)
            bulb.start_flow(Flow(3, Flow.actions.recover, critical_flash))


def warn():
    for bulbn in bulbs:
        if bulbn != '':
            bulb = Bulb(bulbn)
            bulb.start_flow(Flow(3, Flow.actions.recover, warning_flash))


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
    global warn_low, warn_stun, warn_slcd, warn_hex
    warn_low = config.getboolean('dota settings', 'low hp warning')
    warn_stun = config.getboolean('dota settings', 'stunned warning')
    warn_slcd = config.getboolean('dota settings', 'silenced warning')
    warn_hex = config.getboolean('dota settings', 'hexed warning')
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
