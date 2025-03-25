"""
Simple DAQ Controller using VISA library
========================================

This is a clone of the simple_daq driver, but based on VISA using pyvisa and pyvisa-py. It has the same functionality,
but leveraging the capacities of VISA
"""

import visa
from time import sleep, time


rm = visa.ResourceManager('@py')


class SimpleDaq():
    """ Controller for the serial devices that ships with Python for the Lab.
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
        self.rsc = rm.open_resource('ASRL'+port)
        sleep(0.5)

    def idn(self):
        """Identify the device.
        """
        return self.rsc.query("IDN")

    def get_analog_value(self, channel):
        """Gets the value from an analog port.

        :param int port: Port number to read.
        :return int: The value read.
        """
        query_string = 'IN:CH{}'.format(channel)
        value = int(self.rsc.query(query_string))
        return value

    def set_analog_value(self, channel, value):
        """ Sets a voltage to an output port.

        :param int port: Port number. Range depends on device
        :param Quantity value: The output value in Volts.
        """
        value = int(value.m_as('V')/3.3*4095)
        write_string = 'OUT:CH{}:{}'.format(channel, value)
        self.rsc.write(write_string)

    def finalize(self):
        """ Closes the communication with the device.
        """
        if self.rsc is not None:
            self.rsc.close()


if __name__ == "__main__":
    import pint
    ur = pint.UnitRegistry()

    d = SimpleDaq('1')
    # input('Waiting to ready')
    print(d.idn())
    #d.write('OUT:CH0:4000')
    input('Press to read value')
    print(d.get_analog_value(0))
    out_value = ur('3.0V')
    d.set_analog_value(0, out_value)
    sleep(0.5)
    out_value = ur('0V')
    d.set_analog_value(0, out_value)
    d.finalize()