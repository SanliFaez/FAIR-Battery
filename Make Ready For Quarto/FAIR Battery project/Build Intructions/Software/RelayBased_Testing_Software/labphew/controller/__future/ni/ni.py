import PyDAQmx

class niDAQ(PyDAQmx):
    def __init__(self, device_number):
        PyDAQmx.__init__(self)