''' The speaker has a volume and frequency.
    This particlar one also has lights!
'''
from control import Control
from device_status import DeviceStatus

import sn3218

class Speaker(Control):

    MIN_VOLUME = 0
    QUIET_VOLUME = 2
    MAX_VOLUME = 10
    on_mappings = [255 for i in range(10)]
    off_mappings = [0 for i in range(10)]
    
    def __init__(self, control_name):
        'Check if the speaker is available'
        Control.__init__(self, control_name=control_name)
        # Run a hardware check
        self.status = DeviceStatus.UNAVAILABLE
        self.volume = Speaker.QUIET_VOLUME

    def __repr__(self):
        'Useful debug information about the speaker'
        return self.control_name + ' Control'

    def set_volume(self):
        'Change the volume of the speaker'

    def alarm(self):
        'Start the speaker and lights'
        # Also start the lights
        sn3218.output(Speaker.on_mappings)

    def stop_alarm(self):
        'Stop the speaker and lights'
        sn3218.output(Speaker.off_mappings)
