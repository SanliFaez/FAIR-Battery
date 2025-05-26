"""
Lantz based DAQ Controller
==========================
This version of the DAQ controller is built with Lantz. For the time being it has to be considered experimental.
However, Lantz is evolving and will become the standard for Python For The Lab. Lantz is briefly covered in the first
edition of the book, but will be extensively explained in the second edition.

"""

from lantz import Feat, Action, DictFeat

from lantz.messagebased import MessageBasedDriver
from time import sleep

class LantzDaq(MessageBasedDriver):
    DEFAULTS = {
        'ASRL': {
            'baud_rate': 9600,
            'write_termination': '\n',
            'read_termination': '\n',
              },
        'COMMON': {
            'timeout': 10,
              },
        }
    __resource_manager = "@py"

    out_value = [0, 0, 0, 0, 0, 0, 0, 0, 0]

    @Feat()
    def idn(self):
        self.write('IDN')
        sleep(0.5)
        return self.read()

    @DictFeat(keys=list(range(0, 2)), limits=(0, 3.3), units='V')
    def set_output(self, key):
        return self.out_value[key]

    @set_output.setter
    def set_output(self, key, value):
        value = int(value / 3.3 * 4095)
        self.out_value[key] = value
        self.write('OUT:CH{}:{}'.format(key, value))

    @DictFeat(keys=list(range(0,10)), limits=(0, 3.3), units='V')
    def get_input(self, key):
        self.write('IN:CH{}'.format(key))
        sleep(0.5)
        value_bits = int(self.read())
        value_volts = value_bits / 1023
        return value_volts

    @Action()
    def identify(self):
        self.write('DI')


if __name__ == "__main__":
    from lantz.log import log_to_screen, DEBUG
    from time import sleep
    log_to_screen(DEBUG)
    with LantzDaq.via_serial('/dev/ttyACM1') as inst:
        inst.set_output[0] = 0
        sleep(1)
        print("Value in channel 0: {}".format(inst.get_input[0]))
        inst.set_output[0] = 3.3
        sleep(1)
        print("Value in channel 0: {}".format(inst.get_input[0]))
        inst.identify()
