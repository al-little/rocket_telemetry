''' Controller runs commands

'''
import os
import configparser
import datetime
import time
import signal
from envirophat import motion, weather
from camera import Camera, CameraCommand

class Controller(object):
    running = True  # Main loop
    sampleInterval = 0.100  # Default sample interval
    cutoffTime = 5 * 60  # Time to run before stopping program
    commands = []
    log_path = ''
    image_path = ''
    video_path = ''
    camera_present = False
    enviro_present = False
    global log_file
    global camera

    def __init__(self):
        'Initialise the firebase instance and read the config'
        self.running = True  # Main loop
        self.readconfig()

        path = self.log_path + 'log_' + str(datetime.datetime.now().strftime("%Y%m%d-%H%M%S")) + '.csv'

        self.log_file = open(path, "a")
        self.log_file.write("Starting telemetry {0}\n".format(datetime.datetime.utcnow()))


        if self.camera_present:
            self.log_file.write("Starting camera    {0}\n".format(datetime.datetime.utcnow()))
            self.camera = Camera('PI Camera')

        signal.signal(signal.SIGTERM, self.stop)
        signal.signal(signal.SIGHUP, self.ignore)

    '''Detect system terminate'''
    def stop(self, sig, frame):
        print('System shutdown')
        self.camera.stop_video()
        self.log_file.write("System shutdown {0}\n".format(datetime.datetime.utcnow()))
        log_file.close()

    '''Detect system hangup'''
    def ignore(self, sig, frame):
        print('ignoring signal %d\n' % sig)
        self.log_file.write("Ignore signal {0}\n".format(datetime.datetime.utcnow()))

    '''readConfig looks at the defaults.cfg file.'''
    def readconfig(self):
        config = configparser.ConfigParser()
        config.read('defaults.cfg')

        self.image_path = config.get('paths', 'image_path')
        self.video_path = config.get('paths', 'video_path')
        self.log_path = config.get('paths', 'log_path')

        self.camera_present = config.getboolean('devices', 'camera')
        self.enviro_present = config.getboolean('devices', 'enviro')

    '''
    Design:
    Start timer: once the difference in altitude reaches 10 metres.
        Timer should probably run for 3 minutes to capture a flight.
    '''
    def run(self):
        'Main run loop that processes commands and records sensor data'
        print('Running...')
        self.log_file.write("=============================================\n")

        self.log_file.write("Starting main loop {0}\n".format(datetime.datetime.utcnow()))

        if self.camera_present:
            self.camera.start_video(self.video_path)

        if self.enviro_present:
            sea_level = weather.altitude()
        else:
            sea_level = 0

        self.log_file.write("Sea level          {0}\n".format(sea_level))

        last_altitude = 0
        start_clock = False
        parachute_deployed = False
        hit_apogee = False
        timer = 0

        self.log_file.write("=============================================\n")
        self.log_file.write("time,altitude,accel_x,accel_y,accel_z\n")

        while self.running:
            if self.enviro_present:
                altitude = weather.altitude()
                acc_values = [round(x, 2) for x in motion.accelerometer()]

                try:
                    self.log_file.write("{0},{1},{2},{3},{4}\n".format(datetime.datetime.utcnow(),
                                                                       str(altitude - sea_level),
                                                                       str(acc_values[0]),
                                                                       str(acc_values[1]),
                                                                       str(acc_values[2])))
                    self.log_file.flush()
                except:
                    print('logging failed')

                # Start the clock once we pass 10 metres
                if altitude - sea_level > 10:
                    start_clock = True

                # If the height is greater than 10m then start running this check.
                if not hit_apogee and last_altitude < altitude and start_clock:
                    # Our maximum altitude
                    hit_apogee = True
                    print('Apogee')

                # Returning to earth...
                if hit_apogee and altitude <= 90 and not parachute_deployed:
                    parachute_deployed = True
                    print('Deploy parachute')

                last_altitude = altitude

            time.sleep(self.sampleInterval)

            if start_clock:
                timer += self.sampleInterval

                if timer > self.cutoffTime:
                    if self.camera_present:
                        self.log_file.write("Auto shutdown... {0}\n".format(datetime.datetime.utcnow()))
                        self.camera.stop_video()

                    self.log_file.close()
                    self.running = False
