import pyrebase, configparser

class Controller:
    config = {
        "apiKey": "AIzaSyD3nhZRJOMruxzpsWkYIKX9BCN-A4i-LGI",
        "authDomain": "rocket-telemetry.firebaseapp.com",
        "databaseURL": "https://rocket-telemetry.firebaseio.com/",
        "storageBucket": "rocket-telemetry.appspot.com"
    }

    def __init__(self):
        "Read telemetry settings"
        print('init')
        self.firebase = pyrebase.initialize_app(self.config)

        self.readConfig()

    def readConfig(self):
        print('readConfig')
        auth = self.firebase.auth()

        config = configparser.ConfigParser()
        config.read('defaults.cfg')

        username = config.get('auth', 'username')
        password = config.get('auth', 'password')

        self.user = auth.sign_in_with_email_and_password(username, password)

        db = self.firebase.database()

        result = db.child('device_info').get(self.user['idToken'])

        print(result.val())

    def run(self):
        "Get sensors"

        "Find settings"

        "Main loop"
        "   Process Commands - Need a way to simulate (command line?)"
        "       Action (start camera, start gps etc"
        "           If gps is started then calling get readings will give you data"
        "       Log commands"
        "       Update device mode if necessary"
        "           Log device mode change"
        "   "
        "   Get readings"
        "       Log to disk"
        "       If enough samples"
        "           db.child('telemetry/telemetry_0X/data').put"
