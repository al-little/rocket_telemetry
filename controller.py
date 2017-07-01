''' Controller runs commands

'''
import pyrebase
import configparser

class Controller(object):
    config = {
        "apiKey": "AIzaSyD3nhZRJOMruxzpsWkYIKX9BCN-A4i-LGI",
        "authDomain": "rocket-telemetry.firebaseapp.com",
        "databaseURL": "https://rocket-telemetry.firebaseio.com/",
        "storageBucket": "rocket-telemetry.appspot.com"
    }

    def __init__(self):
        'Initialise the firebase instance and read the config'
        self.running = True  # Main loop
        self.user = None  # Required to execute firebase commands
        self.firebase = None
        self.db = None
        self.sampleInterval = 2500  # Default sample interval
        self.sendInterval = 5000  # Default send interval

        self.firebase = pyrebase.initialize_app(self.config)
        self.readconfig()

    def readconfig(self):
        'Read the configuration information from firebase'
        auth = self.firebase.auth()
        config = configparser.ConfigParser()

        # Read the firebase configuration information
        config.read('defaults.cfg')
        username = config.get('auth', 'username')
        password = config.get('auth', 'password')

        # Sign into firebase, to allow reads and writes
        self.user = auth.sign_in_with_email_and_password(username, password)
        self.db = self.firebase.database()

        # Read the device information
        result = self.db.child('device_info').get(self.user['idToken'])
        results = result.val()

        print(results)

        self.sendInterval = results['send_interval']
        self.sampleInterval = results['sample_interval']

    def readcommand(self):
        return False

    def run(self):
        'Main run loop that processes commands and records sensor data'
        print('Running...')
        sampleCount = 0
        # Get sensors

        # Find settings

        while self.running:
            if self.readcommand():
                print('Processing command...')
                # Update firebase if the device mode changes

            print("Collecting samples..." + str(sampleCount))

            sampleCount = sampleCount + self.sampleInterval

            if sampleCount >= self.sendInterval:
                print('[Send samples]')
                sampleCount = 0
