''' The Sensor class can control a physical sensor.
    When in test mode it can give you realistic data.
'''
class Sensor:
    def __init__(self, thing):
        self.name = thing

    def getReading(self):
        return None