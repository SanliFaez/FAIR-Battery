# -*- coding: utf-8 -*-
"""
================
Blink controller
================

This is an example of a controller with a fake (invented) device. It should help to guide
developers to create new controllers for real devices.

Example usage can be found at the bottom of the file under if __name__=='__main___'
"""
import logging
import time

class BlinkController:
    """
    Blink Controller: Fake Device controller to act as an example.
    """
    def __init__(self):
        """
        Create Blink controller object which simulates a fake device.
        """
        self.logger = logging.getLogger(__name__)

        # Set parameters to simulate the device
        self.__simulated_device_blink_period= 1  #
        self.__simulated_device_start_time = time.time()
        self.__simulated_device_status = False
        self.__simulated_device_enabled = True

        # Set user parameters:
        self.max_blink_period = 2
        self.min_blink_period = 0.2

        self.logger.debug('BlinkController object created')
        self.connect()

    def connect(self):
        """
        Fake method to connect to fake blink device

        :return:
        :rtype:
        """
        self.logger.info('"Connected" to fake blink device')

    def set_blink_period(self, period_s):
        """
        Method that mimics setting a device parameter.

        :param period_s: blink period (in seconds)
        :type period_s: float
        """
        # You could do some checks first. For example to see if the value is in an allowed range:
        if period_s > self.max_blink_period:
            self.logger.warning(f'Blink period of {period_s}s exceeds maximum allowed. Setting period to {self.max_blink_period}s')
            period_s = self.max_blink_period
        if period_s < self.min_blink_period:
            self.logger.warning(f'Blink period of {period_s}s exceeds minimum allowed. Setting period to {self.min_blink_period}s')
            period_s = self.min_blink_period
        # Your code to communicate with the device goes here.
        # For the purpose of demonstration, this method simulates setting a parameter on a device:
        self.logger.debug('"Sending" blink period of {} to device'.format(period_s))
        self.__simulated_device_blink_period = period_s
        self.__simulated_device_start_time = time.time()
        self.__simulated_device_status = not self.__simulated_device_status

    def enable(self, enable):
        """
        Method that mimics setting a device parameter.

        :param enable: Enable device output
        :type enable: bool
        """
        # Your code to communicate with the device goes here.
        # For the purpose of demonstration, this method simulates setting a parameter on a device:
        self.__simulated_device_enabled = bool(enable)
        self.logger.debug('Device is "{}"'.format(self.__simulated_device_enabled))

    def get_status(self):
        """
        Method that mimics communicating with a device and retrieving a status.

        :return: True when device is "on"
        :rtype: bool
        """
        # Your code to communicate with the device goes here.
        # For the purpose of demonstration, this method returns a simulated status:
        if self.__simulated_device_enabled:
            return bool(int((time.time()-self.__simulated_device_start_time)/self.__simulated_device_blink_period/.5) % 2)
        else:
            self.logger.warning('Device is disabled')
            return False

    def disconnect(self):
        """
        Fake method to disconnect from fake blink device

        :return:
        :rtype:
        """
        self.logger.info('"Disconnected" from fake blink device')


if __name__ == "__main__":
    import labphew  # Import labphew, for labphew style logging

    device = BlinkController()
    print('The state if the device is:', device.get_status())

    # Example of modifying the blink period:
    device.set_blink_period(3)
    device.set_blink_period(0.1)

    # # Example of acquiring data (the device state) in a for loop and then plotting it with matplotlib: 
    # import matplotlib.pyplot as plt
    # record = []
    # for i in range(100):
    #     time.sleep(0.01)
    #     record.append(device.get_status())
    # plt.plot(record)
