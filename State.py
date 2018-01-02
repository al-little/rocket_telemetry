from enum import Enum

#  Telemetry
#   GPS
#    Camera
#     Beep
#      Pressure
#  12345678
#  00000000

class State(Enum):
    UNINITIALISED = 0
    INITIALISING = 1
    INITIALISED = 2
    STARTED_SILENT = 3
    STARTED_FLASH = 4
    STARTED_BEEP = 5
    STARTED_FLASH_BEEP = 6
    STOPPED_ALARM = 7
    STOPPED_TELEMETRY = 8
    STOPPED_VIDEO = 9