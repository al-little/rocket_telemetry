''' Controls are objects that can do things.
    Typically a speaker or camera.
'''

class Control(object):
    def __init__(self, control_name):
        'Initialise the control with a name'
        self.control_name = control_name