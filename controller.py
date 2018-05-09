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

    "Adding an on and off button"
    "https://grahamwhome.wixsite.com/tetchytechie/single-post/2018/01/10/A-working-Raspberry-Pi-3-power-button"
    "http://www.raspberry-pi-geek.com/Archive/2013/01/Adding-an-On-Off-switch-to-your-Raspberry-Pi"
    running = True  # Main loop
    user = None  # Required to execute firebase commands
    firebase = None
    db = None

    "Capabilites to be read from the configuration file"
    hasSpeaker = False
    hasLights = False
    hasCamera = False
    hasEnviro = False
    has2G = False
    has3G = False
    hasGPS = False

    sampleInterval = 250  # Default sample interval
    sendInterval = 5000  # Default send interval
    commands = []

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

    """readConfig looks at the defaults.cfg file.
    If a Fona board is present then initialise it and detect if we have 3G
    GPS?
    """
    def readconfig(self):
        'Read the configuration information from firebase'
        auth = self.firebase.auth()
        config = configparser.ConfigParser()

        # Read the firebase configuration information
        config.read('defaults.cfg')
        username = config.get('auth', 'username')
        password = config.get('auth', 'password')

        "Read the physically installed inputs and outputs"
        if config.has_option(section='outputs', option='speaker'):
            self.hasSpeaker = True

        if config.has_option(section='outputs', option='lights'):
            self.hasLights = True

        if config.has_option(section='inputs', option='enviro'):
            self.hasEnviro = True

        if config.has_option(section='outputs', option='fona'):
            self.has2G = True

        if self.has2G:
            "Now need to initialise the modem"
            "Ultimately the self.has3G needs to be set"

        if self.has3G and len(username) > 0 and len(password) > 0:
            "Sign into firebase, to allow reads and writes"
            self.user = auth.sign_in_with_email_and_password(username, password)
            self.db = self.firebase.database()

            "Read the device information"
            result = self.db.child('device_info').get(self.user['idToken'])
            results = result.val()

            print(results)

            self.sendInterval = results['send_interval']
            self.sampleInterval = results['sample_interval']

            "self.fileFormat = results['file_fmt']"
            "self.smsNumber = results['tel']"

            "TODO: The camera is capable of annotating text onto the video"
            "Flexible format (new file/telemetry dir || date || time || cool name)"

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
                object = command[0]

                if object == 'C':
                    print('Camera')
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
                    "os.system('sudo shutdown -h now')"

                "Either acknowledge or update firebase"

                "Process: C - Camera, S - Speaker, E - Enviro, A - All"


    def run(self):
        'Main run loop that processes commands and records sensor data'
        print('Running...')
        sampleCount = 0

        "Get installed sensors"

        while self.running:
            self.commands.append(input("Prompt>"))

            self.readcommand()

            print("Collecting samples..." + str(sampleCount))

            if self.hasEnviro:
                "Collect a set of environment values"
                "TODO: Stub"

            if self.hasGPS:
                "Collect a set of GPS coordinates"
                "TODO: Stub"

            sampleCount = sampleCount + self.sampleInterval

            print('[Save samples]')

            if sampleCount >= self.sendInterval:

                if self.has3G:
                    print('[Send samples]')

                sampleCount = 0
