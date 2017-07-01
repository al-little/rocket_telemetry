''' Show the status of a device

'''

from enum import Enum

class DeviceStatus(Enum):
    UNAVAILABLE = 0
    UNINITIALISED = 1
    INITIALISED = 2
    READY = 3
