''' Read data from the environmental sensor
'''
from device_status import DeviceStatus
from envirophat import motion, weather


class EnvironmentSensor(object):
    last_temperature = 0.0
    last_pressure = 0.0
    sea_level_pressure = 0.0
    last_altitude = 0.0

    def __init__(self, sensor_name):
        self.status = DeviceStatus.READY
        self.sensor_name = sensor_name

    '''Get a reading from the environment pHat'''
    def read_values(self):
        x, y, z = motion.accelerometer()
        self.last_temperature = weather.temperature()
        self.last_pressure = weather.pressure()
        self.last_altitude = weather.altitude()

        return x, y, z, self.last_temperature, self.last_pressure, self.last_altitude

    def set_sea_level(self, pressure):
        self.sea_level_pressure = pressure

    '''Get the current altitude. At least one set of values must have been read.
    The sea level must also have been set.
    https://forum.arduino.cc/index.php?topic=63726.0
    '''
    def get_current_altitude(self):
        return ((pow((self.sea_level_pressure / self.last_pressure), 1 / 5.257) - 1.0)
                * (self.last_temperature + 273.15)) / 0.0065

    def get_altitude(self, sea_level, pressure, temperature):
        return ((pow((sea_level / pressure), 1 / 5.257) - 1.0)
                * (temperature + 273.15)) / 0.0065
