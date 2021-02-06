''' Read data from the environmental sensor
'''
from device_status import DeviceStatus
from envirophat import motion, weather


class EnvironmentSensor(object):
    last_temperature = 0.0
    last_pressure = 0.0
    sea_level_pressure = 0.0
    last_altitude = 0.0
    # This value is necessary to calculate the correct height above sealevel
    # its also included in airport weather information ATIS named as QNH
    # The default is equivilent to the air pressure at mean sea level
    # in the International Standard Atmosphere (ISA).
    # See: https://en.wikipedia.org/wiki/Pressure_altitude
    QNH=1013.25 # hpA

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

    def altitude(self, pressure, qnh=QNH):
        """Return the current approximate altitude.
        This calculation is lifted from /enviro-phat/library/envirophat/bmp280.py
        :param pressure: From the sensor
        :param qnh: Your local value for atmospheric pressure adjusted to sea level.
        """
        return 44330.0 * (1.0 - pow(pressure / (qnh*100), (1.0/5.255))) # Calculate altitute from pressure & qnh
