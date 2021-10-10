"""
Analog Discovery 2 View
=======================

MonitorWindow class is used to display continuous stream of live data from the Digilent Analog Discovery 2.
All the processes that are not relating to user interaction are handled by the Operator class in the model folder.

The CC and CV Charge modes work with the hardware described here: https://fair-battery.readthedocs.io/en/latest/technical%20drawings.html#battery-charging-circuit
THe CR and CC Discharge modes work with the hardware describes here: https://fair-battery.readthedocs.io/en/latest/technical%20drawings.html#battery-discharging-circuit

"""
import dwf
import numpy as np
# import pyqtgraph as pg  # used for additional plotting features
from PyQt5 import uic
from PyQt5.QtCore import QTimer, QRectF
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap, QPainter

import ruamel.yaml
import Battery_Testing_Software.labphew
import logging
import os
from time import time
from Battery_Testing_Software.labphew.core.tools.gui_tools import set_spinbox_stepsize, ValueLabelItem
from Battery_Testing_Software.labphew.core.base.general_worker import WorkThread
from Battery_Testing_Software.labphew.core.base.view_base import MonitorWindowBase
from Battery_Testing_Software.labphew.model.analog_discovery_2_model import Operator


class MonitorWindow(MonitorWindowBase):

    def __init__(self, operator: Operator, parent=None):
        """
        Creates the monitor window.
        :param operator: The operator
        :type operator: labphew operator instance
        :param parent: Optional parent GUI
        :type parent: QWidget
        """
        # self.logger = logging.getLogger(__name__)
        super().__init__(parent)
        self.setWindowTitle('Analog Discovery 2')
        self.operator = operator
        self.scan_windows = {}  # If any scan windows are loaded, they will be placed in this dict

        # # For loading a .ui file (created with QtDesigner):
        self.logger.info('Loading UI Elements')
        logging.disable(logging.DEBUG)  # Disable logging for UI Setup
        p = os.path.dirname(__file__)
        uic.loadUi(os.path.join(p, 'UI/BatteryTesterUI.ui'), self)
        logging.disable(logging.NOTSET)  # Re-enable logging
        # For Initializing UI
        self.set_graph()

        # For python generated UI
        # self.set_UI()

        # create thread and timer objects for monitor
        self.monitor_timer = QTimer()
        self.monitor_timer.timeout.connect(self.update_monitor)
        self.monitor_thread = WorkThread(self.operator._monitor_loop)

        # set default tab modes # TODO: either read current tabs or update tabs to these values on startup
        self.test_selection = 0  # Type of test to run: CV (0) / CC (1) / CR (2)
        self.charge_mode = 0    # Whether to Charge or Discharge: Charge (T) / Discharge (F)
        self.test_type = 0  # Charge (0) / Discharge (1) / Impedance (2)
        self.end_time = 0

        self.target_voltage = 0
        self.target_current = 0
        self.target_resistance = 512
        self.out_voltage = self.target_voltage

        self.shunt_resistance = 0.24

        self.max_test_time = 0

    def set_graph(self):
        """Initialize setting for graphs"""
        self.graphicsView.setBackground('k')
        self.plot1 = self.graphicsView.addPlot()
        self.plot1.setLabel('bottom', 'Time', units='s')
        self.plot1.setLabel('left', 'Voltage', units='V')
        self.curve1 = self.plot1.plot(pen='y')
        text_update_time = self.operator.properties['monitor']['text_update_time']
        self.label_1 = ValueLabelItem('--', color='y', siPrefix=True, suffix='V', siPrecision=4,
                                      averageTime=text_update_time, textUpdateTime=text_update_time)
        self.graphicsView.addItem(self.label_1)

    def setup_fields(self):
        pass

    # Define Abstract Methods from Parent

    # GUI Values
    def set_max_test_time(self, max_time):
        """Get time in minutes as float"""
        self.max_test_time = float(max_time)
        self.logger.debug('Test Time: ' + str(int(self.max_test_time * 60)) + " s")

    def set_max_test_voltage(self, max_voltage):
        self.max_test_voltage = max_voltage
        self.logger.debug("Max Test Voltage: " + str(round(max_voltage, 3)) + " V")

    def set_min_test_voltage(self, min_voltage):
        self.min_test_voltage = min_voltage
        self.logger.debug("Min Test Voltage: " + str(round(min_voltage, 3)) + " V")

    def set_target_voltage(self, voltage):
        self.target_voltage = voltage
        self.logger.debug("Target: " + str(round(voltage, 3)) + " V")

    def set_target_current(self, current):
        self.target_current = current
        self.logger.debug("Target: " + str(round(current, 3)) + " mA")

    def set_target_resistance(self, resistance):
        self.target_resistance = resistance
        self.logger.debug("Target: " + str(round(resistance, 3)) + " Ohms")

    def set_target_resistance_finished(self):
        resistances = [512, 225, 131, 65.9, 32.9, 16.9, 8.9]    # Define possible resistances
        desired_resistance = self.target_resistance
        if desired_resistance not in resistances:
            closest_resistance = min(resistances, key=lambda x: abs(x - desired_resistance))  # Find closest resistance to target
            self.target_resistance = closest_resistance
            self.target_resistance_spinbox.setValue(self.target_resistance)     # Update UI to new value
            self.logger.debug("Target: " + str(round(desired_resistance, 3)) + " changed to nearest possible (" + str(round(closest_resistance, 3)) + " Ohms)")

    def set_min_frequency(self, frequency):
        self.logger.debug("Min. Frequency: " + str(frequency) + " Hz")

    def set_max_frequency(self, frequency):
        self.logger.debug("Max. Frequency: " + str(frequency) + " Hz")

    def set_steps_per_decade(self, steps):
        self.logger.debug("Steps per Decade:" + str(steps))

    def set_flow_rate(self, flow_rate):
        self.logger.debug('Flow Rate: ' + str(flow_rate))

    def set_max_test_current(self, current):
        self.logger.debug('Max Test Current: ' + str(current))

    # GUI Actions

    def start_test_button(self):    # TODO: Add voltage check to make sure battery is connected before starting w/ minV
        """
        Called when start button is pressed.
        Starts the monitor (thread and timer) and disables some gui elements
        """
        if self.operator._busy:
            self.logger.debug("Operator is busy")
            return
        else:
            if self.max_test_time > 0:
                self.buffer_time = np.array([])
                self.buffer_voltage = np.array([])
                self.buffer_current = np.array([])
                self.logger.debug('Starting monitor')
                self.operator._allow_monitor = True  # enable operator monitor loop to run
                self.monitor_thread.start()  # start the operator monitor
                self.monitor_timer.start(
                    int(self.operator.properties['monitor']['gui_refresh_time'] * 1000))  # start the update timer
                # Disable UI Elements
                self.start_button.setEnabled(False)
                self.reset_button.setEnabled(False)
                self.charge_radiobutton.setEnabled(False)
                self.discharge_radiobutton.setEnabled(False)
                self.target_selection_tabs.setEnabled(False)
                self.test_mode_tabs.setEnabled(False)
                self.target_voltage_spinbox.setEnabled(False)
                self.target_current_spinbox.setEnabled(False)
                self.target_resistance_spinbox.setEnabled(False)

                self.end_time = time() + (float(self.max_test_time) * 60)
                self.out_voltage = self.operator.instrument.read_analog()[0]  # Start test at measured cell voltage
                if self.test_type == 1:  # If Charge (0) / Discharge (1) / Impedance (2) mode is selected
                    if self.test_selection == 2:  # If CV (0) / CC (1) / CR (2) test is selected
                        self.run_cr_discharge_test(self.target_resistance)
            else:
                self.logger.warning("Set Max. Test Time > 0 to run a test")

    def stop_test_button(self):
        """
        Called when stop button is pressed.
        Stops the monitor:
        - flags the operator to stop
        - uses the Workthread stop method to wait a bit for the operator to finish, or terminate thread if timeout occurs
        """
        # TODO: add method to clean current test instead of this below line
        self.operator.pps_out(0, 0.6)

        if not self.monitor_thread.isRunning():
            self.logger.debug('Monitor is not running')
            return
        else:
            # set flag to to tell the operator to stop:
            self.logger.debug('Stopping monitor')
            self.operator._stop = True
            self.monitor_thread.stop(self.operator.properties['monitor']['stop_timeout'])
            self.operator._allow_monitor = False  # disable monitor again
            self.operator._busy = False  # Reset in case the monitor was not stopped gracefully, but forcefully stopped

    def reset_test_button(self):
        self.logger.debug('Resetting monitor')
        self.curve1.setData((0, 0), (0, 0))
        # self.label_1.setValue(0)
        self.measured_voltage_lineedit.setText("0.00")
        self.measured_current_lineedit.setText("0.00")
        self.operator.pps_out(0, 4)
        pass

    def set_test_selection(self, selection):
        self.test_selection = selection
        self.logger.debug('CV (0) / CC (1) / CR (2): ' + str(selection))

    def set_test_mode(self, impedance_mode):
        if impedance_mode:
            self.test_type = 2
        elif not impedance_mode:
            self.test_type = int(not self.charge_radiobutton.isChecked())
        self.logger.debug('Charge (0) / Discharge (1) / Impedance (2): ' + str(self.test_type))

    def set_charge_mode(self, charge_mode: bool):
        if charge_mode:
            self.test_type = 0
        elif not charge_mode:
            self.test_type = 1
        self.logger.debug('Charge (0) / Discharge (1) / Impedance (2): ' + str(self.test_type))

    def confirmation_box(self, message):  # TODO: Not an abstract method
        """
        Pop-up box for confirming an action.

        :param message: message that will be displayed in pop-up window
        :type message: str
        :return: bool
        """
        ret = QMessageBox.question(self, 'ConfirmationBox', message, QMessageBox.Yes | QMessageBox.No)
        return True if ret == QMessageBox.Yes else False

    def export_raw_data(self):
        self.logger.debug("Saving Raw Data...")
        import numpy
        try:
            a = numpy.asarray([self.buffer_time, self.buffer_voltage, self.buffer_current])

            name, file_type = QFileDialog.getSaveFileName(self, 'Save Raw Data')
            if name:
                filename = name if ".csv" in name else name + ".csv"
                numpy.savetxt(filename, a.T, delimiter=",", header="Time (s), Cell Voltage (V), Current (mA)", fmt='%1.3f')
                self.logger.debug("Test " + filename + " saved")
            else:
                self.logger.error("Raw Data Not Saved")
        except AttributeError:
            self.logger.error("No Data Collected to Export")  # An attribute error will be thrown as there is no self.buffer_time yet when tests have not run

    def export_figure(self):
        self.logger.debug("Saving Figure...")
        name, file_type = QFileDialog.getSaveFileName(self, 'Save Figure')
        if name:
            filename = name if ".png" in name else name + ".png"

            # Get the size of your graphicsView
            rect = self.graphicsView.viewport().rect()
            # Create a pixmap the same size as your graphicsView
            # You can make this larger or smaller if you want.
            pixmap = QPixmap(rect.size())
            painter = QPainter(pixmap)
            # Render the graphicsView onto the pixmap and save it out.
            self.graphicsView.render(painter, QRectF(pixmap.rect()), rect)
            pixmap.save(filename)
            painter.end()
            self.logger.debug("Figure " + filename + " saved")
        else:
            self.logger.error("Figure Not Saved")

    def save_test(self):
        """Save test to test config file. Currently will overwrite current opened test"""
        filename, file_type = QFileDialog.getSaveFileName(self, 'Save Test')
        with open(filename, 'w') as f:
            # TODO: update all self.test_config parameters here
            ruamel.yaml.YAML().dump(self.test_config, f)
            self.logger.debug('Saving Test - Unfinished & UNTESTED')
            f.close()

    def load_test(self):
        """
        This function loads the configuration file to generate the properties of the Test.

        :param filename: Path to the filename. Defaults to analog_discovery_2_config.yml in labphew.core.defaults
        :type filename: str
        """
        filename, file_type = QFileDialog.getOpenFileName(self, 'Load Test')
        with open(filename, 'r') as f:
            self.test_config = ruamel.yaml.safe_load(f)
        self.test_config['config_file'] = filename
        self.update_parameters()

    # Custom Methods for Test Actions

    def update_parameters(self):
        """ Function for updating all test parameters """
        self.title.setText("FAIRBattery Testing Software - " + self.test_config['test_file'])
        self.test_mode_tabs.setCurrentIndex(self.test_config['test']['test_mode'])
        self.target_selection_tabs.setCurrentIndex(self.test_config['test']['test_selection'])
        self.charge_radiobutton.setChecked(self.test_config['test']['charge_mode'])
        self.discharge_radiobutton.setChecked(not self.test_config['test']['charge_mode'])
        self.target_voltage_spinbox.setValue(self.test_config['test']['target_voltage'])
        self.target_current_spinbox.setValue(self.test_config['test']['target_current'])
        self.target_resistance_spinbox.setValue(self.test_config['test']['target_resistance'])
        self.max_time_spinbox.setValue(self.test_config['test']['max_test_time'])
        self.max_cell_voltage_spinbox.setValue(self.test_config['test']['max_test_voltage'])
        self.min_cell_voltage_spinbox.setValue(self.test_config['test']['min_test_voltage'])
        self.max_current_spinbox.setValue(self.test_config['test']['max_current'])
        self.flow_rate_spinbox.setValue(self.test_config['test']['flow_rate'])
        self.shunt_resistance = self.test_config['hardware']['shunt_resistance']
        self.operator._set_monitor_time_step(self.test_config['test']['time_step'])
        self.operator._set_monitor_plot_points(self.test_config['test']['plot_points'])
        self.logger.debug('Parameters Updated')

    def run_cv_charge_test(self, voltage, increment=0.01, margin=0):
        """
        Feedback based; must be repeated throughout test.

        :param voltage: desired voltage
        :param increment: fixed amount to increment voltage per control loop to get desired current
        :param margin: margin in V about where the loop will not react; the "allowed inaccuracy" that prevents the loop
                       from over-controlling
        """
        self.operator.enable_pps(True)
        if self.operator.analog_monitor_1[-1] < voltage - margin:
            self.out_voltage += increment
        elif self.operator.analog_monitor_1[-1] > voltage + margin:
            self.out_voltage -= increment
        self.operator.pps_out(0, self.out_voltage)
        #print(self.out_voltage)

    def run_cc_charge_test(self, current, increment=0.1, margin=5):
        """
        Feedback based; this method must be repeated throughout test.

        :param current: desired charge current
        :param increment: fixed amount to increment voltage per control loop to get desired current
        :param margin: current margin in mA about where the loop will not react; the "allowed inaccuracy" that prevents
                       the loop from over-controlling
        """
        self.operator.enable_pps(True)
        if self.buffer_current[-1] < current - margin:
            self.out_voltage += increment
        elif self.buffer_current[-1] > current + margin:
            self.out_voltage -= increment
        self.operator.pps_out(0, self.out_voltage)
        #print(self.buffer_current[-1], current, self.out_voltage)

    def run_cr_discharge_test(self, resistance: float):
        """
        Only supports resistances mapped to control pins in the below dictionary.
        Only should be run once on start of test.

        :param resistance: desired load resistance
        """
        resistances = {512.0: [],
                       225.0: [8],
                       131.0: [8, 9],
                       65.9: [8, 9, 10],
                       32.9: [8, 9, 10, 11],
                       16.9: [8, 9, 10, 11, 12],
                       8.9: [8, 9, 10, 11, 12, 13]}
        all_pins = resistances[8.9]
        pins = resistances[resistance]
        print(pins)
        for pin in all_pins:    # Turn all pins off
            # self.operator.write_digital(0, pin)
            pass
        for pin in pins:        # Turn desired pins on
            self.operator.write_digital(1, pin)

    def run_cc_discharge_test(self, current):   # TODO: Implement CC discharge
        pass

    def run_impedance_test(self):  # TODO: implement impedance test
        pass

    def apply_properties(self):
        """
        Apply properties dictionary to gui elements.
        """
        self.ao1_label.setText(self.operator.properties['ao'][1]['name'])
        self.ao2_label.setText(self.operator.properties['ao'][2]['name'])

        self.time_step_spinbox.setValue(self.operator.properties['monitor']['time_step'])
        self.plot_points_spinbox.setValue(self.operator.properties['monitor']['plot_points'])

        self.plot1.setTitle(self.operator.properties['monitor'][1]['name'])
        self.plot2.setTitle(self.operator.properties['monitor'][2]['name'])

    def time_step(self):
        """
        Called when time step spinbox is modified.
        Updates the parameter using a method of operator (which checks validity) and forces the (corrected) parameter in the gui element
        """
        self.operator._set_monitor_time_step(self.time_step_spinbox.value())
        self.time_step_spinbox.setValue(self.operator.properties['monitor']['time_step'])
        set_spinbox_stepsize(self.time_step_spinbox)

    def plot_points(self):
        """
        Called when plot points spinbox is modified.
        Updates the parameter using a method of operator (which checks validity) and forces the (corrected) parameter in the gui element
        """
        self.operator._set_monitor_plot_points(self.plot_points_spinbox.value())
        self.plot_points_spinbox.setValue(self.operator.properties['monitor']['plot_points'])
        set_spinbox_stepsize(self.plot_points_spinbox)

    def update_monitor(self):
        """
        Checks if new data is available and updates the graph.
        Checks if thread is still running and if not: stops timer and reset gui elements
        (called by timer)
        """
        from datetime import timedelta
        if self.operator._new_monitor_data:
            self.operator._new_monitor_data = False
            self.curve1.setData(self.operator.analog_monitor_time, self.operator.analog_monitor_1)
            self.label_1.setValue(self.operator.analog_monitor_1[-1])
            self.measured_voltage_lineedit.setText(str(round(self.operator.analog_monitor_2[-1], 2)))
            shunt_voltage = self.operator.analog_monitor_2[-1] - self.operator.analog_monitor_1[-1]
            shunt_voltage = shunt_voltage if shunt_voltage > 0 else 0
            self.current = round((shunt_voltage / self.shunt_resistance) * 1000, 2)
            self.measured_current_lineedit.setText(str(self.current))
            time_elapsed = timedelta(seconds=round(self.operator.analog_monitor_time[-1], 1))

            timestr = str(time_elapsed).split('.')  # TODO: this section needs a one-liner
            if len(timestr) == 1:
                timestr.append("00")
            else:
                timestr[1] = timestr[1][0:2]
            self.time_elapsed_value.setText(".".join(timestr))

            self.buffer_time = np.append(self.buffer_time, self.operator.analog_monitor_time[-1])
            self.buffer_voltage = np.append(self.buffer_voltage, self.operator.analog_monitor_1[-1])
            self.buffer_current = np.append(self.buffer_current, self.current)

        if time() >= self.end_time:
            self.stop_test_button()

        # TODO: implement discharge function
        if self.test_type == 0:     # If Charge (0) / Discharge (1) / Impedance (2) mode is selected
            if self.test_selection == 0:    # If CV (0) / CC (1) / CR (2) test is selected
                self.run_cv_charge_test(self.target_voltage)
            elif self.test_selection == 1:  # If CV (0) / CC (1) / CR (2) test is selected
                self.run_cc_charge_test(self.target_current)

        elif self.test_type == 1:   # If Charge (0) / Discharge (1) / Impedance (2) mode is selected
            if self.test_selection == 1:    # If CV (0) / CC (1) / CR (2) test is selected
                self.run_cc_discharge_test(self.target_resistance)

        elif self.test_type == 2:   # If Charge (0) / Discharge (1) / Impedance (2) mode is selected
            self.run_impedance_test()

        if self.monitor_thread.isFinished():
            self.logger.debug('Monitor thread is finished')
            self.monitor_timer.stop()
            # RE-Enable UI Elements
            self.start_button.setEnabled(True)
            self.reset_button.setEnabled(True)
            self.charge_radiobutton.setEnabled(True)
            self.discharge_radiobutton.setEnabled(True)
            self.target_selection_tabs.setEnabled(True)
            self.test_mode_tabs.setEnabled(True)
            self.target_voltage_spinbox.setEnabled(True)
            self.target_current_spinbox.setEnabled(True)
            self.target_resistance_spinbox.setEnabled(True)

    def closeEvent(self, event):
        """ Gets called when the window is closed. Could be used to do some cleanup before closing. """

        # Use this bit to display an "Are you sure" dialog popup
        quit_msg = "Are you sure you want to exit Battery Tester?"
        reply = QMessageBox.question(self, 'Message', quit_msg, QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.No:
            event.ignore()
            return
        self.stop_monitor()  # stop monitor if it was running
        self.monitor_timer.stop()  # stop monitor timer, just to be nice
        # Close all child scan windows
        for scan_win in self.scan_windows.values():
            scan_win[0].close()
        self.operator.disconnect_devices()
        event.accept()


if __name__ == "__main__":
    import Battery_Testing_Software.labphew  # import this to use labphew style logging
    import sys
    from PyQt5.QtWidgets import QApplication

    logging.info('Connecting to AD2 Device')
    # To use with real device
    from Battery_Testing_Software.labphew.controller.digilent.waveforms import DfwController

    # To test with simulated device
    # from labphew.controller.digilent.waveforms import SimulatedDfwController as DfwController
    # TODO: add simulated device functions
    try:
        instrument = DfwController()
        opr = Operator(instrument)  # Create operator instance
        opr.load_config()
    except dwf.DWFError as err:
        logging.info(str(err) + "Could not connect to AD2 Device. Exiting...")
        exit(-1)

    import platform
    if platform.system() == 'Darwin':
        os.environ['QT_MAC_WANTS_LAYER'] = '1'  # added to fix operation on mac

    app = QApplication(sys.argv)
    app_icon = QIcon(os.path.join(Battery_Testing_Software.labphew.package_path, 'view', 'design',
                                  '../../labphew/view/design/icons', 'labphew_icon.png'))
    app.setWindowIcon(app_icon)  # set an app icon
    gui = MonitorWindow(opr)
    gui.show()
    sys.exit(app.exec_())
