
import configparser
import datetime
import time
import signal
from envirophat import motion, weather
from camera import Camera


class Controller(object):
    running = True
    sampleInterval = 0.100  # Default sample interval
    cutoffTime = 1 * 60  # Time to run before stopping program
    safe_start_altitude = 3.0  # Altitude where the shutdown timer starts
    parachute_deply_altitude = 90  # Altitude to deploy the secondary parachute
    log_path = ''
    image_path = ''
    video_path = ''
    camera_present = False
    enviro_present = False
    global log_file
    global camera

    def __init__(self):
        'Read the config'
        self.running = True  # Main loop
        self.readconfig()

        path = self.log_path + 'log_' + str(datetime.datetime.now().strftime("%Y%m%d-%H%M%S")) + '.csv'

        self.log_file = open(path, "a")
        self.log_file.write("=============================================\n")
        self.log_file.write("{0} image_path {1}\n".format(datetime.datetime.utcnow(), self.image_path))
        self.log_file.write("{0} video_path {1}\n".format(datetime.datetime.utcnow(), self.video_path))
        self.log_file.write("{0} log_path {1}\n".format(datetime.datetime.utcnow(), self.log_path))
        self.log_file.write("{0} Camera present {1}\n".format(datetime.datetime.utcnow(), self.camera_present))
        self.log_file.write("{0} Enviro present {1}\n".format(datetime.datetime.utcnow(), self.enviro_present))

        if self.camera_present:
            self.log_file.write("{0} Starting camera\n".format(datetime.datetime.utcnow()))
            self.camera = Camera('PI Camera')

        signal.signal(signal.SIGTERM, self.stop)
        signal.signal(signal.SIGHUP, self.ignore)

    '''Detect system terminate'''
    def stop(self, sig, frame):
        print('System shutdown')
        self.camera.stop_video()
        self.log_file.write("{0} System shutdown\n".format(datetime.datetime.utcnow()))
        log_file.close()

    '''Detect system hangup'''
    def ignore(self, sig, frame):
        print('ignoring signal %d\n' % sig)
        self.log_file.write("{0} Ignore signal\n".format(datetime.datetime.utcnow()))

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
        self.log_file.write("{0} Starting telemetry capture\n".format(datetime.datetime.utcnow()))

        if self.camera_present:
            self.camera.start_video(self.video_path)

        if self.enviro_present:
            sea_level = weather.altitude()
        else:
            sea_level = 0.0

        self.log_file.write("Sea level          {0}\n".format(sea_level))

        start_clock = False
        parachute_deployed = False
        hit_apogee = False
        timer = 0
        max_altitude = 0.0
        max_acc_x = 0.0
        max_acc_y = 0.0
        max_acc_z = 0.0
        parachute_deployed_at = None
        apogee_reached_at = None 

        self.log_file.write("=============================================\n")
        self.log_file.write("time,altitude,accel_x,accel_y,accel_z\n")

        while self.running:
            if self.enviro_present:
                altitude = weather.altitude()
                acc_values = [round(x, 2) for x in motion.accelerometer()]

                if acc_values[0] > max_acc_x:
                    max_acc_x = acc_values[0]
                if acc_values[1] > max_acc_y:
                    max_acc_y = acc_values[1]
                if acc_values[2] > max_acc_z:
                    max_acc_z = acc_values[2]

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
            if start_clock == False and altitude - sea_level > self.safe_start_altitude:
                print('Starting clock')
                start_clock = True

            if altitude > max_altitude:
                max_altitude = altitude

            if start_clock and altitude < max_altitude - 1 and not hit_apogee:
                # Our maximum altitude - 1 metre
                hit_apogee = True
                apogee_reached_at = datetime.datetime.utcnow()
                print('Apogee: ' + str(max_altitude) + ' metres')

            # Is it time to deploy a secondary parachute?
            if hit_apogee and altitude <= self.parachute_deply_altitude and not parachute_deployed:
                parachute_deployed = True
                parachute_deployed_at = datetime.datetime.utcnow()
                print('Deploy secondary parachute')

            time.sleep(self.sampleInterval)

            if start_clock:
                timer += self.sampleInterval

                print('Timer: ' + str(timer) + ' of ' + str(self.cutoffTime))

                if timer > self.cutoffTime:
                    self.log_file.write("=============================================\n")
                    self.log_file.write("{0} Auto shutdown\n".format(datetime.datetime.utcnow()))
                    self.log_file.write("{0} Max altitude: {1}\n".format(datetime.datetime.utcnow(), max_altitude - sea_level))
                    if not apogee_reached_at is None:
                        self.log_file.write("{0} Apogee at: {1}\n".format(datetime.datetime.utcnow(), apogee_reached_at))
                    self.log_file.write("{0} Max acceleration: x{1} y{2} z{3}\n".format(datetime.datetime.utcnow(), max_acc_x, max_acc_y, max_acc_z))

                    if not parachute_deployed_at is None:
                        self.log_file.write("{0} Secondary parachute deployed at {1}\n".format(datetime.datetime.utcnow(), parachute_deployed_at))

                    if self.camera_present:
                        self.log_file.write("{0} Shutdown camera...\n".format(datetime.datetime.utcnow()))
                        self.camera.stop_video()

                    self.log_file.write("=============================================\n")
                    self.log_file.close()
                    self.running = False
