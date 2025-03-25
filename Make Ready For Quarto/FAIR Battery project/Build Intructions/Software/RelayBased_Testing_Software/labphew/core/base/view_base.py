# coding=utf-8
"""
View Base Classes
=================

Base class for View Windows.
- When the object of the child class is created the base class checks if required and recommended methods are present
  in the child class (and in the base class itself).
- By inheriting, methods from this base class will be used if they are missing in the child class. This allows to
  implement some fallback functionality and to warn the user.
- In addition it implements the __enter__ and __exit__ methods to allow the class to be used in a python with block.

Example usage can be found at the bottom of the file under if __name__=='__main___'
"""

from Battery_Testing_Software.labphew.core.base.tools import check_method_presence_and_warn
from Battery_Testing_Software.labphew.core.tools.gui_tools import fit_on_screen, ModifyConfig
import logging
import os.path
import yaml
from PyQt5.QtWidgets import QMainWindow, QAction

class MonitorWindowBase(QMainWindow):
    def __new__(cls, *args, **kwargs):
        """
        Get's called before the object (of the child class) is created and warns if required or
        recommended methods are missing in that class.
        Note that required and recommended methods may exist in this Base class.
        """
        required = ['__init__']
        recommended = ['closeEvent', 'load_scan_guis', 'open_scan_window', 'start_monitor', 'stop_monitor', 'update_monitor']
        check_method_presence_and_warn(cls, required, recommended)
        return super().__new__(cls)

    def __init__(self, parent=None, *args, **kwargs):
        self.logger = logging.getLogger(self.__module__)  # creating a logger (just in case)
        super().__init__(parent)

    def closeEvent(self, event):
        """ Gets called when the window is closed. Could be used to do some cleanup before closing. """
        self.logger.warning(f"Your {self.__class__.__name__} class doesn't have a closeEvent method (using the method from MonitorWindowBase)")
        try:
            self.stop_monitor()
            self.monitor_timer.stop()
        except: pass
        try:
            for scan_win in self.scan_windows.values():
                scan_win[0].close()
        except: pass
        try:
            self.operator.disconnect_devices()
        except: pass
        event.accept()

    # the next two methods are needed so the context manager 'with' works.
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """ This method get's called when exiting a python with block (when the code completed but also when an error occured)"""
        self.logger.debug('Calling disconnect_devices() before exiting with block')
        self.disconnect_devices()

    # It is actually fine to use this method from te base class and not re-implement it in your own
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

    # It is actually fine to use this method from te base class and not re-implement it in your own
    def open_scan_window(self):
        """
        This method is called by the menu and opens Scan Windows that were "attached" to this Monitor gui with load_scan_guis().
        """
        self.stop_monitor()
        name = self.sender().text()  # get the name of the QAction (which is also the key of the scanwindow dictionary)
        self.logger.debug('Opening scan window {}'.format(name))
        self.scan_windows[name][0].show()
        fit_on_screen(self.scan_windows[name][0])

    def start_monitor(self):
        self.logger.warning(f"Using start_monitor method from MonitorWindowBase, it's strongly recommended that you create a start_monitor method in your {self.__class__.__name__} class.")
        try:
            if self.operator._busy:
                self.logger.debug("Operator is busy")
                return
            else:
                self.logger.debug('Starting monitor')
                self.operator._allow_monitor = True  # enable operator monitor loop to run
                self.monitor_thread.start()  # start the operator monitor
                self.monitor_timer.start(self.operator.properties['monitor']['gui_refresh_time'])  # start the update timer
        except:
            pass

    def stop_monitor(self):
        self.logger.warning(f"Using stop_monitor method from MonitorWindowBase, it's strongly recommended that you create a stop_monitor method in your {self.__class__.__name__} class.")
        try:
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
        except:
            pass

    def update_monitor(self):
        self.logger.warning(f"update_monitor method is missing in {self.__class__.__name__} class.")



class ScanWindowBase(QMainWindow):
    def __new__(cls, *args, **kwargs):
        """
        Get's called before the object (of the child class) is created and warns if required or
        recommended methods are missing in that class.
        Note that required and recommended methods may exist in this Base class.
        """
        required = ['__init__']
        recommended = ['closeEvent', 'mod_scan_config', 'reset_fields', 'start_scan', 'pause_scan', 'stop_scan', 'kill_scan', 'update_scan']
        check_method_presence_and_warn(cls, required, recommended)
        return super().__new__(cls)

    def __init__(self, parent=None, *args, **kwargs):
        self.logger = logging.getLogger(self.__module__)  # creating a logger (just in case)
        super().__init__(parent)

    def closeEvent(self, event):
        """ Gets called when the window is closed. Could be used to do some cleanup before closing. """
        self.logger.warning(f"Your {self.__class__.__name__} class doesn't have a closeEvent method (using the method from ScanWindowBase)")
        try:
            self.stop_scan()  # stop scan
            self.scan_timer.stop()
        except:
            pass
        event.accept()

    # the next two methods are needed so the context manager 'with' works.
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """ This method get's called when exiting a python with block (when the code completed but also when an error occured)"""
        self.logger.debug('Calling disconnect_devices() before exiting with block')
        self.disconnect_devices()

    # It's kind of ok to inherit this as long as your callback method is called apply_properties (if you need a callback)
    def mod_scan_config(self):
        self.logger.info(f"Your {self.__class__.__name__} class is missing the the recommended mod_scan_config method.")
        if hasattr(self, 'apply_properties'):
            callback = self.apply_properties
        else:
            callback = None
        conf_win = ModifyConfig(self.operator.properties['scan'], apply_callback=callback, parent=self)
        conf_win.show()

    def reset_fields(self):
        self.logger.warning(
            f"Your {self.__class__.__name__} class is missing the the reset_fields method. Use that to reset gui elements and flags after a scan")
        self.operator._busy = False
        self.operator._pause = False
        self.operator._stop = False

    def start_scan(self):
        self.logger.warning(f"start_scan method is missing in {self.__class__.__name__} class.")
        try:
            if self.operator._busy:
                self.logger.debug("Operator is busy")
                return
            else:
                self.logger.debug('Starting scan')
                self.scan_thread.start()  # start the operator monitor
                try:
                    self.scan_timer.start(self.operator.properties['scan']['gui_refresh_time'])  # start the update timer
                except:
                    try:
                        self.scan_timer.start(0.05)  # start the update timer
                    except:
                        pass
        except:
            pass

    def pause_scan(self):
        self.logger.warning(f"pause_scan method is missing in {self.__class__.__name__} class.")
        try:
            self.operator._pause = not self.operator._pause
        except:
            pass

    def stop_scan(self):
        self.logger.warning(f"stop_scan method is missing in {self.__class__.__name__} class.")

        try:
            self.logger.debug('Stopping operator')
            self.operator._stop = True
            if self.scan_thread.isRunning():
                self.scan_thread.stop(self.operator.properties['scan']['stop_timeout'])
        except:
            pass
        try:
            self.operator._busy = False  # Reset in case the monitor was not stopped gracefully, but forcefully stopped
            self.reset_fields()
        except:
            pass

    def kill_scan(self):
        self.logger.warning(f"kill_scan method is missing in {self.__class__.__name__} class.")
        try:
            self.operator._stop = True
            self.scan_thread.terminate()
            self.reset_fields()
        except:
            pass

    def update_scan(self):
        self.logger.warning(f"update_scan method is missing in {self.__class__.__name__} class.")