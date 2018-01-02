''' The Sensor class can control a physical sensor.
    When in test mode it can give you realistic data.
'''
from device_status import DeviceStatus

class Sensor(object):
    def __init__(self, sensor_name):
        'Every sensor has state and data'
        self.status = DeviceStatus.UNAVAILABLE
        self.sensor_name = sensor_name

    def getReading(self):
        'Get a reading from the sensor'
        return None