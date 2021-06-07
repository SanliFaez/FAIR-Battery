# coding=utf-8
"""
Analog Discovery 2
==================

This module contains an example class of an Operator for the Digilent Analog discovery 2

This Operator contains:
- basic methods to get analog in values, set analog out values
- a monitor, to provide continuous data for a Monitor gui
- an example of a scan that could be run from command line or from a Scan gui

Example usage can be found at the bottom of the file under if __name__=='__main___'
"""
import os.path
import numpy as np
import yaml
from time import time, sleep, localtime, strftime
import logging
import xarray as xr
from datetime import datetime
from labphew.core.base.operator_base import OperatorBase
import labphew


class Operator(OperatorBase):
    """
    Example Operator class for Digilent Analog Discovery 2.
    """
    def __init__(self, instrument, properties={}):
        """
        Create the Operator object for the Digilent Analog Discovery 2.
        The DigilentWaveForms controller object for the instrument needs to be created before and passed as an argument.

        :param instrument: The instrument used by this Operator
        :type instrument: DigilentWaveForms controller object
        :param properties: optional properties dictionary, note that this can be loaded from file with load_config()
        :type properties: dict
        """
        self.logger = logging.getLogger(__name__)
        self.properties = properties
        self.instrument = instrument

        # Flags controlled by operator:
        self._busy = False  # indicates the operator is busy (e.g. with scan or monitor)
        self._new_scan_data = False  # signal there's new data that could be displayed (a gui would reset this to False after retrieving the data)
        self._new_monitor_data = False  # used to flag gui that new data is available

        # Flags controlled by external gui to control flow of loops (e.g. scan or monitor)
        self._stop = False  # signal a loop to stop (whenever operator is not busy it should be False)
        self._pause = False  # signal a loop to pause (whenever operator is not busy it should be False)
        self._allow_monitor = False  # monitor should not be run from command line, a gui can set this to True

        self._monitor_start_time = 0
        self.monitor_plot_points = 100
        # Create direct alias for this method of the instrument:
        self.analog_in = self.instrument.read_analog

    def analog_out(self, channel, value=None, verify_only=False):
        """
        Set analog_out.
        Forces value to be in allowed range.
        Applies the value to the output channel.
        Returns the (corrected) value.
        Note: if verify_only is set True it does not apply the value, but only return the corrected value

        :param channel: channel 1 or 2
        :type channel: int
        :param value: voltage to set (in Volt)
        :type value: float
        :param verify_only: if True it does not apply the value to the channel (default: False)
        :type verify_only: bool
        :return: the value set to the channel
        :rtype: float
        """
        if channel not in [1, 2]:
            self.logger.error('incorrect channel number')
            return
        upr = self.properties['ao'][channel]['upper_limit']
        lwr = self.properties['ao'][channel]['lower_limit']
        if value > upr:
            self.logger.info(f'{value} exceeds ch{channel} limit, clipping to {upr}')
            value = upr
        elif value < lwr:
            self.logger.info(f'{value} exceeds ch{channel} limit, clipping to {lwr}')
            value = lwr
        if not verify_only:
            self.instrument.write_analog(value, channel-1)
        return value

    # Nic Added #
    def pps_out(self, channel, value=0, verify_only=False):
        """
        Set pps_out.
        Forces value to be in allowed range.
        Applies the value to the output channel.
        Returns the (corrected) value.
        Note: if verify_only is set True it does not apply the value, but only return the corrected value

        :param channel: channel 0 or 1 (V+ or V-)
        :type channel: int
        :param value: voltage to set (in Volt)
        :type value: float
        :param verify_only: if True it does not apply the value to the channel (default: False)
        :type verify_only: bool
        :return: the value set to the channel
        :rtype: float
        """
        if channel not in [0, 1]:
            self.logger.error('incorrect channel number')
            return
        # upr = self.properties['ao'][channel]['upper_limit']
        # lwr = self.properties['ao'][channel]['lower_limit']
        # if value > upr:
        #     self.logger.info(f'{value} exceeds ch{channel} limit, clipping to {upr}')
        #     value = upr
        # elif value < lwr:
        #     self.logger.info(f'{value} exceeds ch{channel} limit, clipping to {lwr}')
        #     value = lwr
        if not verify_only:
            self.instrument.write_pps(value, channel)
        return value

    def enable_pps(self, enable=True):
        self.instrument.enable_pps(enable)

    def _set_monitor_time_step(self, time_step):
        """
        Set Monitor time step.
        Forces the value to be at least 0.01, and warns for large values

        :param time_step: time step between acquisitions in the monitor loop (seconds)
        :type time_step: float
        """
        if time_step < 0.01:
            time_step = 0.01
            self.logger.warning(f"time_step too small, setting: {time_step}s")
        elif time_step> 2:
            self.logger.warning(f"setting time_step to {time_step}s (are you sure?)")
        self.properties['monitor']['time_step'] = time_step

    def _set_monitor_plot_points(self, plot_points):
        """
        Set number of plot points for Monitor.
        Forces the value to be at least 2, and warns for large values.

        :param plot_points: time step between acquisitions in the monitor loop (seconds)
        :type plot_points: int
        """
        if plot_points < 2:
            plot_points = 2
            self.logger.warning(f"points too low, setting: {plot_points}s")
        elif plot_points > 200:
            self.logger.warning(f"setting plot_points to {plot_points}s (are you sure?)")
        self.properties['monitor']['plot_points'] = plot_points

    def _verify_scan_channels(self):
        """
        Checks if channels in properties are valid and returns analog out and analog in channel.
        Note that None is returned if an error is found

        :return:  analog out and analog in channel of scan
        :rtype: (int, int)
        """
        if 'scan' not in self.properties:
            self.logger.error("'scan' not found in properties")
            return
        if 'ao_channel' not in self.properties['scan'] or self.properties['scan']['ao_channel'] not in [1,2]:
            self.logger.error("'ao_channel' not found in properties or invalid value (should be 1 or 2)")
            return
        if 'ai_channel' not in self.properties['scan'] or self.properties['scan']['ai_channel'] not in [1,2]:
            self.logger.error("'ai_channel' not found in properties or invalid value (should be 1 or 2)")
            return
        return self.properties['scan']['ao_channel'], self.properties['scan']['ai_channel']

    def _set_scan_start(self, value):
        """
        Set scan start value.
        Forces value to be in valid range and updates properties dictionary.
        Also corrects the sign of step if required.

        :param value: start value of scan (V)
        :type value: float
        """
        ao_ch, _ = self._verify_scan_channels()
        if ao_ch is None:  # if _verify_scan_channels() returns nothing that means channel is invalid or not found
            return
        value = self.analog_out(ao_ch, value, verify_only=True)
        self.properties['scan']['start'] = value
        self._set_scan_step()

    def _set_scan_stop(self, value):
        """
        Set scan stop value.
        Forces value to be in valid range and updates properties dictionary.

        :param value: stop value of scan (V)
        :type value: float
        """
        ao_ch, _ = self._verify_scan_channels()
        if ao_ch is None:  # if _verify_scan_channels() returns nothing that means channel is invalid or not found
            return
        value = self.analog_out(ao_ch, value, verify_only=True)
        self.properties['scan']['stop'] = value
        self._set_scan_step()

    def _set_scan_step(self, step=None):
        """
        Set scan step value. Note that it will correct the sign automatically accroding to start and stop values.
        If no step value is supplied it only corrects the sign of step.

        :param step: the stepsize for the scan (V)
        :type step: float or None
        """
        if step == 0:
            self.logger.warning('stepsize of 0 is not possible')
            return
        if step is not None:
            self.properties['scan']['step'] = step
        if np.sign(self.properties['scan']['step']) != np.sign(self.properties['scan']['stop'] - self.properties['scan']['start']):
            self.properties['scan']['step'] *= -1

    def _monitor_loop(self):
        """
        Called by GUI Monitor to start the monitor loop.
        Not intended to be called from Operator. (Which should be blocked)
        """
        # First check if monitor is allowed to start
        if self._busy or not self._allow_monitor:
            self.logger.warning('Monitor should only be run from GUI and not while Operator is busy')
            return
        try:
            # Preparations before running the monitor
            self.analog_monitor_1 = np.zeros(self.properties['monitor']['plot_points'])
            self.analog_monitor_2 = np.zeros(self.properties['monitor']['plot_points'])
            # self.analog_monitor_time = np.zeros(self.properties['monitor']['plot_points'])
            self.analog_monitor_time = np.arange(1-self.properties['monitor']['plot_points'], 1)*self.properties['monitor']['time_step']
        except:
            self.logger.error("'plot_points' or 'time_step' missing or invalid in config")
            return
        self._busy = True  # set flag to indicate operator is busy
        self._monitor_start_time = time()
        next_time = 0
        while not self._stop:
            timestamp = time() - self._monitor_start_time
            analog_in = self.instrument.read_analog()  # read the two analog in channels
            # To keep the length constant, roll/shift the buffers and add the new datapoints
            self.analog_monitor_1 = np.roll(self.analog_monitor_1, -1)
            self.analog_monitor_2 = np.roll(self.analog_monitor_2, -1)
            self.analog_monitor_time = np.roll(self.analog_monitor_time, -1)
            self.analog_monitor_1[-1] = analog_in[0]
            self.analog_monitor_2[-1] = analog_in[1]
            self.analog_monitor_time[-1] = timestamp
            self._new_monitor_data = True
            # in stead of sleep, calculate when the next datapoint should be acquired and wait until that time arrives
            # this allows to keep the timing correct
            next_time += self.properties['monitor']['time_step']
            while time()-self._monitor_start_time<next_time:
                if self._stop: break  # check for stop flag while waiting to move to next point
        self._stop = False  # reset stop flag to false
        self._busy = False  # indicate the operator is not busy anymore

    def do_scan(self, param=None):
        """
        An example of a method that performs a scan (based on parameters in the config file).
        This method can be run from a GUI, from command line or other script
        This scan sweeps the voltage on one of the AO channels and reads one of the AI channels.

        :param param: optional dictionary of parameters that will used to update the scan parameters
        :type param: dict
        :return: the AO voltage, and the measured AI voltages
        :rtype: list, list
        """
        if type(param) is dict:
            self.logger.info('Updating scan properties with supplied parameters dictionary.')
            self.properties['scan'].update(param)
        # Start with various checks and warn+return if something is wrong
        if self._busy:
            self.logger.error('Scan should not be started while Operator is busy.')
            return
        if 'scan' not in self.properties:
            self.logger.error("The config file or properties dict should contain 'scan' section.")
            return
        required_keys = ['start', 'stop', 'step', 'ao_channel', 'ai_channel']
        if not all(key in self.properties['scan'] for key in required_keys):
            self.logger.error("'scan' should contain: "+', '.join(required_keys))
            return
        try:
            start = self.properties['scan']['start']
            stop = self.properties['scan']['stop']
            step = self.properties['scan']['step']
            ch_ao = int(self.properties['scan']['ao_channel'])
            ch_ai = int(self.properties['scan']['ai_channel'])
        except:
            self.logger.error("Error occured while reading scan config values")
            return
        if ch_ai not in [1,2] or ch_ao not in [1,2]:
            self.logger.error("AI and AO channel need to be 1 or 2")
            return
        if 'stabilize_time' in self.properties['scan']:
            stabilize = self.properties['scan']['stabilize_time']
        else:
            self.logger.info("stabilize_time not found in config, using 0s")
            stabilize = 0
        num_points = np.int(round( (stop-start)/step+1 ))  # use round to catch the occasional rounding error
        if num_points <= 0:
            self.logger.error("Start, stop and step result in 0 or fewer points to sweep")
            return

        self.voltages_to_scan = np.linspace(start, stop, num_points)

        self.scan_voltages = []
        self.measured_voltages = []

        self._busy = True  # indicate that operator is busy

        for i, voltage in enumerate(self.voltages_to_scan):
            self.logger.debug('applying {} to ch {}'.format(voltage, ch_ao))
            self.analog_out(ch_ao, voltage)
            sleep(stabilize)
            measured = self.analog_in()[ch_ai - 1]
            self.measured_voltages.append(measured)
            self.scan_voltages.append(voltage)

            # The remainder of the loop adds functionality to plot data and pause and stop the scan when it's run from a gui:
            self._new_scan_data = True
            # before the end of the loop: halt if pause is True
            while self._pause:
                sleep(0.05)
                if self._stop: break
            # if (soft) stop was requested, break out of loop
            if self._stop:
                break

        self._stop = False  # reset stop flag to false
        self._busy = False  # indicate operator is not busy anymore
        self._pause = False  # is this necessary?

        return self.scan_voltages, self.measured_voltages

    def save_scan(self, filename, metadata=None, store_conf=False):
        """
        Store data in xarray Dataset and save to netCDF4 file.
        Optional metadata can be passed as a dict. Note that the keys should be strings and the values should be numbers or strings.
        Optionally stores the entire Operator properties dictionary to a yaml file of the same name.

        To load data:
        import xarray as xr
        xr.load_dataset(filename)

        :param filename: full path and filename
        :type filename: str
        :param metadata: optional additional data to store (default: None)
        :type metadata: dict
        :param store_conf: store Operator properties in yaml file (default: False)
        :type store_conf: bool
        """
        # First test if the required data arrays have been generated (i.e. if the scan has run)
        if not hasattr(self, "scan_voltages") or not hasattr(self, "measured_voltages"):
            self.logger.warning('no data to save yet')
            return
        if os.path.exists(filename):
            self.logger.warning('overwriting existing file: {}'.format(filename))
        self.logger.debug('Saving data')
        data = xr.Dataset(
            coords={
                "scan_voltage": (["scan_voltage"], self.scan_voltages, {"units": 'V'})
            },
            data_vars={
                "measured_voltage": (["scan_voltage"], self.measured_voltages, {"units":'V'})
            },
            attrs={
                "time": datetime.now().strftime('%d-%m-%YT%H:%M:%S'),
            }
        )
        for key in ['user', 'config_file']:
            if key in self.properties:
                data.attrs[key] = self.properties[key]
        # Add all numeric and string keys
        for key, value in self.properties['scan'].items():
            if isinstance(value, (int, float, bool, str)):
                data.attrs[key] = value
        if type(metadata) is dict:
            data.attrs.update(metadata)  # add the optional metadata to the Dataset attributes
        self.data = data
        data.to_netcdf(filename)
        self.logger.info('Data saved in {}'.format(filename))

        if store_conf:
            try:
                self.logger.info('Storing Operator properties in yaml file')
                yml_fname = os.path.splitext(filename)[0] + '.yml'
                with open(yml_fname, 'w') as f:
                    yaml.safe_dump(self.properties, f)
            except:
                self.logger.warning('An error occurred while trying to save Operator properties to yaml file')

    def disconnect_devices(self):
        """
        Close connection to all instruments/devices used by this operator.
        (Note that this method will get called when exiting a python with block)
        """
        # This method is included because it is recommended (this method gets called when closing the gui), but the
        # WaveForms controller does not have a disconnect, hence this method does nothing.
        self.logger.info('Disconnecting from device(s)')

    def load_config(self, filename=None):
        """
        If specified, this function loads the configuration file to generate the properties of the Scan.

        :param filename: Path to the filename. Defaults to analog_discovery_2_config.yml in labphew.core.defaults
        :type filename: str
        """
        if filename and not os.path.isfile(filename):
            self.logger.error('Config file not found: {}, falling back to default'.format(filename))
            filename = None

        if filename is None:
            filename = os.path.join(labphew.package_path, 'core', 'defaults', 'analog_discovery_2_config.yml')
        with open(filename, 'r') as f:
            self.properties.update(yaml.safe_load(f))
        self.properties['config_file'] = filename


if __name__ == "__main__":
    import labphew   # import this to use labphew style logging (by importing it before matplotlib it also prevents matplotlib from printing many debugs)
    import matplotlib.pyplot as plt

    # from labphew.controller.digilent.waveforms import DfwController

    # To import the actual device:
    from labphew.controller.digilent.waveforms import DfwController

    # To import a simulated device:
    # from labphew.controller.digilent.waveforms import SimulatedDfwController as DfwController

    instrument = DfwController()

    opr = Operator(instrument)
    opr.load_config()

    x, y = opr.do_scan()
    plt.plot(x,y)
