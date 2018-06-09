''' Controller runs commands

'''
import os
import configparser
import datetime
import time
import random
from envirophat import motion, weather
from camera import Camera, CameraCommand

class Controller(object):
    "Adding an on and off button"
    "https://grahamwhome.wixsite.com/tetchytechie/single-post/2018/01/10/A-working-Raspberry-Pi-3-power-button"
    "http://www.raspberry-pi-geek.com/Archive/2013/01/Adding-an-On-Off-switch-to-your-Raspberry-Pi"
    running = True  # Main loop
    log_path = ''

    sampleInterval = 0.100  # Default sample interval
    sendInterval = 5000  # Default send interval
    commands = []
    image_path = ''
    video_path = ''
    camera = Camera('PI Camera')

    def __init__(self):
        'Initialise the firebase instance and read the config'
        self.running = True  # Main loop
        self.readconfig()

    """readConfig looks at the defaults.cfg file.
    If a Fona board is present then initialise it and detect if we have 3G
    GPS?
    """
    def readconfig(self):
        'Read the configuration information from firebase'
        config = configparser.ConfigParser()

        # Read the firebase configuration information
        config.read('defaults.cfg')
        self.image_path = config.get('paths', 'image_path')
        self.video_path = config.get('paths', 'video_path')
        self.log_path = config.get('paths', 'log_path')

    def readcommand(self):
        while len(self.commands) > 0:
            "Update firebase if the device mode changes"
            "Play noise/Update lights to reflect state"
            "Start new session"
            "   Create a new directory ready for data"
            "Stop current session"
            command = self.commands.pop()

            print('Processing command: [' + command + ']')

            if len(command) > 0:
                object = command[0].upper()

                if object == 'C':
                    if len(command) > 1:
                        try:
                            cmd = CameraCommand(int(command[1]))

                            if cmd == CameraCommand.STILL_PHOTO:
                                self.camera.take_picture(self.image_path)
                            elif cmd == CameraCommand.START_VIDEO:
                                self.camera.start_video(self.video_path)
                            elif cmd == CameraCommand.STOP_VIDEO:
                                self.camera.stop_video()
                            break
                        except ValueError:
                            print('Unrecognised Camera Command')
                elif object == 'S':
                    print('Speaker')
                elif object == 'E':
                    print('Enviro')
                elif object == 'A':
                    print('All')
                    if len(command) > 1:
                        cmd = command[1]

                        if cmd == '1':
                            print('All on')
                            "Collect samples, start video"
                        else:
                            print('All off')
                elif object == '0':
                    print('System message')
                    "Reset, Shutdown"
                    os.system('sudo shutdown -h now')

                "Either acknowledge or update firebase"

                "Process: C - Camera, S - Speaker, E - Enviro, A - All"


    def run(self):
        'Main run loop that processes commands and records sensor data'
        print('Running...')
        path = self.log_path + 'log_' + str(datetime.datetime.now().strftime("%Y%m%d-%H%M%S")) + '.csv'

        log = open(path, "a")

        'initial altitude'
        sea_level = 0
        altitude = 0
        last_altitude = 0
        accel_x = 0
        accel_y = 0
        accel_z = 0

        while self.running:
            self.commands.append(input("Command >"))
            self.readcommand()

            altitude = weather.altitude()

            if sea_level == 0:
                sea_level = altitude

            acc_values = [round(x, 2) for x in motion.accelerometer()]

            accel_x = acc_values[0]
            accel_y = acc_values[1]
            accel_z = acc_values[2]

            try:
                log.write("{0},{1},{2},{3},{4}\n".format(datetime.datetime.utcnow(),
                                                         str(altitude - sea_level),
                                                         str(accel_x),
                                                         str(accel_y),
                                                         str(accel_z)))
            except:
                print('logging failed')

            if last_altitude < altitude:
                print('Apogee')

            last_altitude = altitude
            time.sleep(self.sampleInterval)

            log.flush()
