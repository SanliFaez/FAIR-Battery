"""
Analog Discovery 2 View
=======================

This module contains 2 classes which are intended to work with a specific Operator (in this case
labphew.model.analog_discovery_2_model.Operator )

MonitorWindow class is used to display continuous stream of live data from the Digilent Analog Discovery 2.
All the processes that are not relating to user interaction are handled by the Operator class in the model folder.

ScanWindow class is used to control and visualize a specific scan defined in the Operator. Note that scan itself is
performed in the Operator and the ScanWindow is only used to modify parameters, start/stop and visualize data.

These Windows may be run separately, but it's also possible to add the ScanWindow (or multiple ScanWindows) to the
MonitorWindow.

Examples of how to use can be found at the end of the file under if __name__=='__main__'

"""

import pyqtgraph as pg   # used for additional plotting features
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
import labphew
import logging
import os
from time import time
from labphew.core.tools.gui_tools import set_spinbox_stepsize, ValueLabelItem, SaverWidget, ModifyConfig, fit_on_screen
from labphew.core.base.general_worker import WorkThread
from labphew.core.base.view_base import MonitorWindowBase, ScanWindowBase
os.environ['QT_MAC_WANTS_LAYER'] = '1'  # added to fix operation on mac

class MonitorWindow(MonitorWindowBase):
    def __init__(self, operator, parent=None):
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
        # p = os.path.dirname(__file__)
        # uic.loadUi(os.path.join(p, 'design/UI/main_window.ui'), self)

        self.set_UI()

        # create thread and timer objects for monitor
        self.monitor_timer = QTimer()
        self.monitor_timer.timeout.connect(self.update_monitor)
        self.monitor_thread = WorkThread(self.operator._monitor_loop)

    def set_UI(self):
        """ Code-based generation of the user-interface based on PyQT """

        self.setWindowTitle('Digilent AD2')
        # display statusbar
        self.statusBar()
        ### The menu bar:
        quit_action = QAction("E&xit", self, triggered=self.close, shortcut="Alt+F4", statusTip='Close the scan window')
        self.mainMenu = self.menuBar()
        fileMenu = self.mainMenu.addMenu('&File')
        fileMenu.addAction(quit_action)

        ### General layout
        central_widget = QWidget()
        central_layout = QHBoxLayout(central_widget)

        # Layout for left hand controls
        control_layout = QVBoxLayout()

        ### Analog Out
        box_ao = QGroupBox('Analog Out')
        layout_ao = QFormLayout()
        box_ao.setLayout(layout_ao)
        control_layout.addWidget(box_ao)

        self.ao1_spinbox = QDoubleSpinBox()
        self.ao1_spinbox.setSuffix('V')
        self.ao1_spinbox.setMinimum(-100)  # limits are checked by the Operator
        self.ao1_spinbox.valueChanged.connect(self.ao1_value)
        self.ao1_spinbox.setDecimals(3)
        self.ao1_spinbox.setSingleStep(0.001)

        self.ao2_spinbox = QDoubleSpinBox()
        self.ao2_spinbox.setSuffix('V')
        self.ao2_spinbox.setMinimum(-100)  # limits are checked by the Operator
        self.ao2_spinbox.valueChanged.connect(self.ao2_value)
        self.ao2_spinbox.setDecimals(3)
        self.ao2_spinbox.setSingleStep(0.001)

        self.ao1_label = QLabel()
        self.ao2_label = QLabel()
        layout_ao.addRow(self.ao1_label, self.ao1_spinbox)
        layout_ao.addRow(self.ao2_label, self.ao2_spinbox)

        ### Monitor
        box_monitor = QGroupBox('Monitor')
        layout_monitor = QVBoxLayout()
        box_monitor.setLayout(layout_monitor)
        control_layout.addWidget(box_monitor)

        layout_monitor_form  = QFormLayout()
        layout_monitor.addLayout(layout_monitor_form)
        layout_monitor_buttons = QHBoxLayout()
        layout_monitor.addLayout(layout_monitor_buttons)

        self.time_step_spinbox = QDoubleSpinBox()
        self.time_step_spinbox.setSuffix('s')
        self.time_step_spinbox.setMinimum(.01)
        self.time_step_spinbox.valueChanged.connect(self.time_step)
        self.time_step_spinbox.setSingleStep(0.01)
        layout_monitor_form.addRow(QLabel('Time step'), self.time_step_spinbox)

        self.plot_points_spinbox = QSpinBox()
        self.plot_points_spinbox.setMinimum(2)
        self.plot_points_spinbox.setMaximum(1000)
        self.plot_points_spinbox.valueChanged.connect(self.plot_points)
        self.plot_points_spinbox.setSingleStep(10)
        layout_monitor_form.addRow(QLabel('Plot points'), self.plot_points_spinbox)

        self.start_button = QPushButton('Start')
        self.start_button.clicked.connect(self.start_monitor)
        self.stop_button = QPushButton('Stop')
        self.stop_button.clicked.connect(self.stop_monitor)

        layout_monitor_buttons.addWidget(self.start_button)
        layout_monitor_buttons.addWidget(self.stop_button)

        ### Graphs:
        self.graph_win = pg.GraphicsWindow()
        self.graph_win.resize(1000, 600)

        self.plot1 = self.graph_win.addPlot()
        self.plot1.setLabel('bottom', 'time', units='s')
        self.plot1.setLabel('left', 'voltage', units='V')
        self.curve1 = self.plot1.plot(pen='y')
        text_update_time = self.operator.properties['monitor']['text_update_time']
        self.label_1 = ValueLabelItem('--', color='y', siPrefix=True, suffix='V', siPrecision=4,
                                      averageTime=text_update_time, textUpdateTime=text_update_time)
        self.graph_win.addItem(self.label_1)

        self.graph_win.nextRow()
        self.plot2 = self.graph_win.addPlot()
        self.plot2.setLabel('bottom', 'time', units='s')
        self.plot2.setLabel('left', 'voltage', units='V')
        self.curve2 = self.plot2.plot(pen='c')
        self.label_2 = ValueLabelItem('--', color='c', siPrefix=True, suffix='V', siPrecision=4,
                                      averageTime=text_update_time, textUpdateTime=text_update_time)
        self.graph_win.addItem(self.label_2)
        self._last_values_update_time = time()

        # Add an empty widget at the bottom of the control layout to make layout nicer
        dummy = QWidget()
        dummy.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        control_layout.addWidget(dummy)
        # Add control layout and graph window to central layout and apply central layout to window
        central_layout.addLayout(control_layout)
        central_layout.addWidget(self.graph_win)
        self.setCentralWidget(central_widget)

        self.apply_properties()

        # To make it look a bit nicer at the beginning (this is not strictly necessary):
        left = -self.operator.properties['monitor']['plot_points'] * self.operator.properties['monitor']['time_step']
        self.plot1.setXRange(left, 0)
        self.plot2.setXRange(left, 0)
        self.plot1.enableAutoRange()
        self.plot2.enableAutoRange()

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

    def load_scan_guis(self, scan_windows):
        """
        Load scan windows and add them to a menu in this monitor window.
        Note that the scan windows should be instantiated before adding them.
        The keys of the dictionary should be strings that will act as the names in the Scan menu.
        The values of the dictionary could be the ScanWindowObjects or a list that also contains some PyQt gui settings
        in a dictionary: [ScanWindowObject, {'shortcut':"Ctrl+Shift+V", 'statusTip':'Voltage sweep scan'}]

        :param scan_windows: scan windows dict
        :type scan_windows: dict
        """
        scanMenu = self.mainMenu.addMenu('&Scans')
        for name, scan_lst in scan_windows.items():
            if type(scan_lst) is not list:
                scan_lst = [scan_lst]
            if len(scan_lst) < 2:
                scan_lst.append({})
            self.scan_windows[name] = scan_lst
            scanMenu.addAction(QAction(name, self, triggered=self.open_scan_window, **scan_lst[1]))

    def open_scan_window(self):
        """
        This method is called by the menu and opens Scan Windows that were "attached" to this Monitor gui with load_scan_guis().
        """
        self.stop_monitor()
        name = self.sender().text()  # get the name of the QAction (which is also the key of the scanwindow dictionary)
        self.logger.debug('Opening scan window {}'.format(name))
        self.scan_windows[name][0].show()
        fit_on_screen(self.scan_windows[name][0])

    def ao1_value(self):
        """
        Called when AO Channel 2 spinbox is modified.
        Updates the parameter using a method of operator (which checks validity) and forces the (corrected) parameter in the gui element
        """
        value = self.operator.analog_out(1, self.ao1_spinbox.value())
        self.ao1_spinbox.setValue(value)
        set_spinbox_stepsize(self.ao1_spinbox)

    def ao2_value(self):
        """
        Called when AO Channel 2 spinbox is modified.
        Updates the parameter using a method of operator (which checks validity) and forces the (corrected) parameter in the gui element
        """
        value = self.operator.analog_out(2, self.ao2_spinbox.value())
        self.ao2_spinbox.setValue(value)
        set_spinbox_stepsize(self.ao2_spinbox)

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

    def start_monitor(self):
        """
        Called when start button is pressed.
        Starts the monitor (thread and timer) and disables some gui elements
        """
        if self.operator._busy:
            self.logger.debug("Operator is busy")
            return
        else:
            self.logger.debug('Starting monitor')
            self.operator._allow_monitor = True  # enable operator monitor loop to run
            self.monitor_thread.start()  # start the operator monitor
            self.monitor_timer.start(self.operator.properties['monitor']['gui_refresh_time'])  # start the update timer
            self.plot_points_spinbox.setEnabled(False)
            self.start_button.setEnabled(False)

    def stop_monitor(self):
        """
        Called when stop button is pressed.
        Stops the monitor:
        - flags the operator to stop
        - uses the Workthread stop method to wait a bit for the operator to finish, or terminate thread if timeout occurs
        """
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

    def update_monitor(self):
        """
        Checks if new data is available and updates the graph.
        Checks if thread is still running and if not: stops timer and reset gui elements
        (called by timer)
        """
        if self.operator._new_monitor_data:
            self.operator._new_monitor_data = False
            self.curve1.setData(self.operator.analog_monitor_time, self.operator.analog_monitor_1)
            self.curve2.setData(self.operator.analog_monitor_time, self.operator.analog_monitor_2)
            self.label_1.setValue(self.operator.analog_monitor_1[-1])
            self.label_2.setValue(self.operator.analog_monitor_2[-1])

        if self.monitor_thread.isFinished():
            self.logger.debug('Monitor thread is finished')
            self.monitor_timer.stop()
            self.plot_points_spinbox.setEnabled(True)
            self.start_button.setEnabled(True)

    def closeEvent(self, event):
        """ Gets called when the window is closed. Could be used to do some cleanup before closing. """

        # # Use this bit to display an "Are you sure"-dialogbox
        # quit_msg = "Are you sure you want to exit labphew monitor?"
        # reply = QMessageBox.question(self, 'Message', quit_msg, QMessageBox.Yes, QMessageBox.No)
        # if reply == QMessageBox.No:
        #     event.ignore()
        #     return
        self.stop_monitor()  # stop monitor if it was running
        self.monitor_timer.stop()  # stop monitor timer, just to be nice
        # Close all child scan windows
        for scan_win in self.scan_windows.values():
            scan_win[0].close()
        self.operator.disconnect_devices()
        event.accept()


class ScanWindow(ScanWindowBase):
    def __init__(self, operator, parent=None):
        self.logger = logging.getLogger(__name__)
        super().__init__(parent)
        self.setWindowTitle('Analog Discovery 2')
        self.operator = operator

        # # For loading a .ui file (created with QtDesigner):
        # p = os.path.dirname(__file__)
        # uic.loadUi(os.path.join(p, 'design/UI/main_window.ui'), self)

        self.set_UI()

        # create thread and timer objects for scan
        self.scan_timer = QTimer(timeout=self.update_scan)
        self.scan_thread = WorkThread(self.operator.do_scan)

    def set_UI(self):
        """
        Code-based generation of the user-interface based on PyQT
        """

        self.setWindowTitle('Digilent AD2 Scan example')
        # display statusbar
        self.statusBar()
        ### The menu bar:
        mod_config_action = QAction("Con&fig", self, triggered=self.mod_scan_config, shortcut="Ctrl+Shift+C", statusTip='Modify the scan config')
        quit_action = QAction("&Close", self, triggered=self.close, shortcut="Ctrl+W", statusTip='Close the scan window')

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('&File')
        fileMenu.addAction(mod_config_action)
        fileMenu.addAction(quit_action)

        ### General layout
        central_widget = QWidget()
        central_layout = QHBoxLayout(central_widget)

        # Layout for left hand controls
        control_layout = QVBoxLayout()

        ### Scan box
        self.box_scan = QGroupBox('Scan')
        layout_scan = QVBoxLayout()
        self.box_scan.setLayout(layout_scan)
        control_layout.addWidget(self.box_scan)

        layout_scan_form = QFormLayout()
        layout_scan.addLayout(layout_scan_form)
        layout_scan_buttons = QHBoxLayout()
        layout_scan.addLayout(layout_scan_buttons)

        self.scan_start_spinbox = QDoubleSpinBox(suffix='V', minimum=-100, singleStep=0.001, valueChanged=self.scan_start_value)
        # self.scan_start_spinbox.valueChanged.connect(self.scan_start_value)

        self.scan_stop_spinbox = QDoubleSpinBox(suffix='V', minimum=-100, singleStep=0.001, valueChanged=self.scan_stop_value)

        self.scan_step_spinbox = QDoubleSpinBox(suffix='V', minimum=-100, singleStep=0.001, valueChanged=self.scan_step_value)

        self.scan_start_label = QLabel('start')
        self.scan_stop_label = QLabel('stop')
        self.scan_step_label = QLabel('step')
        layout_scan_form.addRow(self.scan_start_label, self.scan_start_spinbox)
        layout_scan_form.addRow(self.scan_stop_label, self.scan_stop_spinbox)
        layout_scan_form.addRow(self.scan_step_label, self.scan_step_spinbox)

        self.start_button = QPushButton('Start', clicked=self.start_scan)
        self.pause_button = QPushButton('Pause', clicked=self.pause_scan)
        self.stop_button = QPushButton('Stop', clicked=self.stop_scan)
        self.kill_button = QPushButton('Kill', clicked=self.kill_scan)
        # Haven't decided what names are best. Suggestions:
        # start, pause, interrupt, stop, abort, quit, kill

        layout_scan_buttons.addWidget(self.start_button)
        layout_scan_buttons.addWidget(self.pause_button)
        layout_scan_buttons.addWidget(self.stop_button)
        layout_scan_buttons.addWidget(self.kill_button)

        self.saver = SaverWidget(self.operator.save_scan)
        layout_scan.addWidget(self.saver)

        ### Graphs:
        self.graph_win = pg.GraphicsWindow()
        self.graph_win.resize(1000, 600)
        self.plot1 = self.graph_win.addPlot()
        self.curve1 = self.plot1.plot(pen='y')

        # Add an empty widget at the bottom of the control layout to make layout nicer
        dummy = QWidget()
        dummy.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        control_layout.addWidget(dummy)
        # Add control layout and graph window to central layout and apply central layout to window
        central_layout.addLayout(control_layout)
        central_layout.addWidget(self.graph_win)
        self.setCentralWidget(central_widget)

        self.apply_properties()
        self.reset_fields()

    def mod_scan_config(self):
        """
        Open the Modify Config window for the scan properties
        """
        conf_win = ModifyConfig(self.operator.properties['scan'], apply_callback=self.apply_properties, parent=self)
        conf_win.show()

    def apply_properties(self):
        """
        Apply properties dictionary to gui elements.
        """
        self.logger.debug('Applying config properties to gui elements')
        self.operator._set_scan_start(self.operator.properties['scan']['start'])  # this optional line checks validity
        self.scan_start_spinbox.setValue(self.operator.properties['scan']['start'])

        self.operator._set_scan_stop(self.operator.properties['scan']['stop'])  # this optional line checks validity
        self.scan_stop_spinbox.setValue(self.operator.properties['scan']['stop'])

        self.operator._set_scan_step(self.operator.properties['scan']['step'])  # this optional line checks validity
        self.scan_step_spinbox.setValue(self.operator.properties['scan']['step'])

        if 'title' in self.operator.properties['scan']:
            self.box_scan.setTitle(self.operator.properties['scan']['title'])
            self.plot1.setTitle(self.operator.properties['scan']['title'])

        self.plot1.setLabel('bottom', self.operator.properties['scan']['x_label'], units=self.operator.properties['scan']['x_units'])
        self.plot1.setLabel('left', self.operator.properties['scan']['y_label'], units=self.operator.properties['scan']['y_units'])
        self.plot1.setXRange(self.operator.properties['scan']['start'], self.operator.properties['scan']['stop'])

        if 'filename' in self.operator.properties['scan']:
            self.saver.filename.setText(self.operator.properties['scan']['filename'])

    def scan_start_value(self):
        """
        Called when Scan Start spinbox is modified.
        Updates the parameter using a method of operator (which checks validity and also fixes the sign of step) and
        forces the (corrected) parameter in the gui elements
        """
        self.operator._set_scan_start(self.scan_start_spinbox.value())
        self.scan_start_spinbox.setValue(self.operator.properties['scan']['start'])
        self.scan_step_spinbox.setValue(self.operator.properties['scan']['step'])
        set_spinbox_stepsize(self.scan_start_spinbox)
        self.plot1.setXRange(self.operator.properties['scan']['start'], self.operator.properties['scan']['stop'])

    def scan_stop_value(self):
        """
        Called when Scan Stop spinbox is modified.
        Updates the parameter using a method of operator (which checks validity and also fixes the sign of step) and
        forces the (corrected) parameter in the gui elements
        """
        self.operator._set_scan_stop(self.scan_stop_spinbox.value())
        self.scan_stop_spinbox.setValue(self.operator.properties['scan']['stop'])
        self.scan_step_spinbox.setValue(self.operator.properties['scan']['step'])
        set_spinbox_stepsize(self.scan_stop_spinbox)
        self.plot1.setXRange(self.operator.properties['scan']['start'], self.operator.properties['scan']['stop'])

    def scan_step_value(self):
        """
        Called when Scan Step spinbox is modified.
        Updates the parameter using a method of operator (which checks validity) and forces the (corrected) parameter in the gui element
        """
        self.operator._set_scan_step(self.scan_step_spinbox.value())
        self.scan_step_spinbox.setValue(self.operator.properties['scan']['step'])
        set_spinbox_stepsize(self.scan_step_spinbox)

    def reset_fields(self):
        """
        Resets gui elements after a scan is finished, stopped or terminated.
        """
        self.start_button.setEnabled(True)
        self.pause_button.setText('Pause')
        self.pause_button.setEnabled(False)
        self.stop_button.setEnabled(False)
        self.scan_start_spinbox.setEnabled(True)
        self.scan_stop_spinbox.setEnabled(True)
        self.scan_step_spinbox.setEnabled(True)
        # Reset all flow control flags
        self.operator._busy = False
        self.operator._pause = False
        self.operator._stop = False

    def start_scan(self):
        """
        Called when start button is pressed.
        Starts the monitor (thread and timer) and disables some gui elements
        """
        if self.operator._busy:
            self.logger.debug("Operator is busy")
            return
        else:
            self.logger.debug('Starting scan')
            self.start_button.setEnabled(False)
            self.pause_button.setEnabled(True)
            self.stop_button.setEnabled(True)
            # self.operator._stop = False  # enable operator monitor loop to run
            self.scan_thread.start()  # start the operator monitor
            self.scan_timer.start(self.operator.properties['scan']['gui_refresh_time'])  # start the update timer
            self.scan_start_spinbox.setEnabled(False)
            self.scan_stop_spinbox.setEnabled(False)
            self.scan_step_spinbox.setEnabled(False)

    def pause_scan(self):
        """
        Called when pause button is clicked.
        Signals the operator scan to pause. Updates buttons accordingly
        """
        if not self.operator._pause:
            self.operator._pause = True
            self.pause_button.setText('Continue')
        else:
            self.operator._pause = False
            self.pause_button.setText('Pause')

    def stop_scan(self):
        """
        Stop all loop threads:
        - flags the operator to stop
        - uses the Workthread stop method to wait a bit for the operator to finish, or terminate thread if timeout occurs
        """
        self.logger.debug('Stopping operator')
        self.stop_button.setEnabled(False)
        self.operator._stop = True
        if self.scan_thread.isRunning():
            self.scan_thread.stop(self.operator.properties['scan']['stop_timeout'])
        self.operator._busy = False  # Reset in case the monitor was not stopped gracefully, but forcefully stopped
        self.reset_fields()

    def kill_scan(self):
        """
        Forcefully terminates the scan thread
        """
        self.logger.debug('Killing operator threads')
        self.operator._stop = True
        self.scan_thread.terminate()
        self.reset_fields()

    def update_scan(self):
        """
        Checks if new data is available and updates the graph.
        Checks if thread is still running and if not: stops timer and reset gui elements
        (called by timer)
        """
        if self.operator._new_scan_data:
            self.operator._new_scan_data = False
            self.curve1.setData(self.operator.scan_voltages, self.operator.measured_voltages)
        if self.scan_thread.isFinished():
            self.logger.debug('Scan thread is finished')
            self.scan_timer.stop()
            self.reset_fields()

    def closeEvent(self, event):
        """ Gets called when the window is closed. Could be used to do some cleanup before closing. """

        # # Use this bit to display an "Are you sure"-dialogbox
        # quit_msg = "Are you sure you want to exit labphew monitor?"
        # reply = QMessageBox.question(self, 'Message', quit_msg, QMessageBox.Yes, QMessageBox.No)
        # if reply == QMessageBox.No:
        #     event.ignore()
        #     return
        self.stop_scan()  # stop scan
        self.scan_timer.stop()  # stop scan timer, just to be sure
        event.accept()


if __name__ == "__main__":
    import labphew  # import this to use labphew style logging

    import sys
    from PyQt5.QtWidgets import QApplication
    from labphew.model.analog_discovery_2_model import Operator

    # To use with real device
    from labphew.controller.digilent.waveforms import DfwController

    # To test with simulated device
    # from labphew.controller.digilent.waveforms import SimulatedDfwController as DfwController

    instrument = DfwController()
    opr = Operator(instrument)
    opr.load_config()

    create_scan_window_only = False  ##### Toggle this to showcase the scanwindow or the monitor

    if create_scan_window_only:
        app = QApplication(sys.argv)
        app_icon = QIcon(os.path.join(labphew.package_path, 'view', 'design', 'icons', 'labphew_icon.png'))
        app.setWindowIcon(app_icon)  # set an icon
        gui = ScanWindow(opr)
        gui.show()
        app.exit(app.exec_())
        app.closeAllWindows()  # close any child window that might have been open
    else:
        # Create a PyQt application
        app = QApplication(sys.argv)
        app_icon = QIcon(os.path.join(labphew.package_path, 'view', 'design', 'icons', 'labphew_icon.png'))
        app.setWindowIcon(app_icon)  # set an icon
        gui = MonitorWindow(opr)
        # To add Scan window(s) to the Monitor window use the following code.
        add_scan_to_monitor = True  ##### Toggle this to showcase monitor with and without scanwindow
        if add_scan_to_monitor:
            scan_1 = ScanWindow(opr, parent=gui)
            scans = {
                'Sweep &voltage': [scan_1, {'shortcut':"Ctrl+Shift+V", 'statusTip':'Voltage sweep scan'}]  # note that the dictionary is optional
                     }
            gui.load_scan_guis(scans)
        gui.show()  # make sure the GUI will be displayed
        app.exit(app.exec_())  # run the application
        app.closeAllWindows()  # close any child window that might have been open

