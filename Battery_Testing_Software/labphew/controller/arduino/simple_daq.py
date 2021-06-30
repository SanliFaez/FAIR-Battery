"""
Simple DAQ Controller
=====================

Python For The Lab revolves around controlling a simple DAQ device built on top of an Arduino.
The DAQ device is capable of generating up to two analog outputs in the range 0-3.3V and to acquire
several analog inputs.

Because of the pedagogy of the course Python for the Lab, it was assumed that the device can generate
value by value and not a sequence. This forces the developer to think on how to implement a solution
purely on Python.
"""

import serial
from time import sleep, time


class SimpleDaq():
    """ Controller for the serial devices that ships with Python for the Lab.
    """
    DEFAULTS = {'write_termination': '\n',
                'read_termination': '\n',
                'encoding': 'ascii',
                'baudrate': 9600,
                'write_timeout': 1,
                'read_timeout': 1,
                }
    """Dictionary storing the defaults to communicate through the serial port.
    """
    rsc = None
    """Resource. It is the actual library providing low level communication. """

    def __init__(self, port):
        """ Automatically initializes the communication with the device.
        """
        self.initialize(port)

    def initialize(self, port):
        """ Opens the serial port with the DEFAULTS.
        """
        self.rsc = serial.Serial(port=port,
                                 baudrate=self.DEFAULTS['baudrate'],
                                 timeout=self.DEFAULTS['read_timeout'],
                                 write_timeout=self.DEFAULTS['write_timeout'])
        sleep(0.5)

    def idn(self):
        """Identify the device.
        """
        return self.query("IDN")

    def get_analog_value(self, channel):
        """Gets the value from an analog port.

        :param int port: Port number to read.
        :return int: The value read.
        """
        query_string = 'IN:CH{}'.format(channel)
        value = int(self.query(query_string))
        return value

    def set_analog_value(self, channel, value):
        """ Sets a voltage to an output port.

        :param int port: Port number. Range depends on device
        :param Quantity value: The output value in Volts.
        """
        value = int(value.m_as('V')/3.3*4095)
        write_string = 'OUT:CH{}:{}'.format(channel, value)
        self.write(write_string)

    def finalize(self):
        """ Closes the communication with the device.
        """
        if self.rsc is not None:
            self.rsc.close()

    def query(self, message):
        """Sends a message to the devices an reads the output.

        :param str message: Message sent to the device. It should generate an output, or it will timeout waiting to read from it.
        :return str: The message read from the device
        """
        self.write(message)
        return self.read()

    def write(self, message):
        """ Writes a message to the device using the DEFAULT end of line and encoding.

        :param str message: The message to send to the device
        """
        if self.rsc is None:
            raise Warning("Trying to write to device before initializing")

        msg = (message + self.DEFAULTS['write_termination']).encode(self.DEFAULTS['encoding'])
        self.rsc.write(msg)
        sleep(0.1)

    def read(self):
        """ Reads from the device using the DEFAUTLS end of line and encoding.

        :return str: The message received from the device.
        """
        line = "".encode(self.DEFAULTS['encoding'])
        read_termination = self.DEFAULTS['read_termination'].encode(self.DEFAULTS['encoding'])

        t0 = time()
        new_char = "".encode(self.DEFAULTS['encoding'])
        while new_char != read_termination:
            new_char = self.rsc.read(size=1)
            line += new_char
            if time()-t0 > self.DEFAULTS['read_timeout']:
                raise Exception("Readout time reached when reading from the device")

        return line.decode(self.DEFAULTS['encoding'])

if __name__ == "__main__":
    import pint
    ur = pint.UnitRegistry()

    d = SimpleDaq('/dev/ttyACM0')
    # input('Waiting to ready')
    print(d.query('IDN'))
    #d.write('OUT:CH0:4000')
    input('Press to read value')
    print(d.query('IN:CH0'))
    out_value = ur('3.0V')
    d.set_analog_value(0, out_value)
    d.finalize()