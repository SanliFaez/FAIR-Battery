# coding=utf-8
"""
Operator Base Class
===================

Base class for operators.
- When the object of the child class is created the base class checks if required and recommended methods are present
  in the child class (and in the base class itself).
- By inheriting, methods from this base class will be used if they are missing in the child class. This allows to
  implement some fallback functionality and to warn the user.
- In addition it implements the __enter__ and __exit__ methods to allow the class to be used in a python with block.

Example usage can be found at the bottom of the file under if __name__=='__main___'
"""

from Battery_Testing_Software.labphew.core.base.tools import check_method_presence_and_warn
import logging
import os.path
import yaml



class OperatorBase:
    def __new__(cls, *args, **kwargs):
        """
        Get's called before the object (of the child class) is created and warns if required or
        recommended methods are missing in that class.
        Note that required and recommended methods may exist in this Base class.
        """
        required = ['__init__']
        recommended = ['load_config', 'disconnect_devices', '_monitor_loop', 'save_scan', 'do_scan']
        check_method_presence_and_warn(cls, required, recommended)
        return super().__new__(cls)

    def __init__(self, *args, **kwargs):
        self.logger = logging.getLogger(self.__module__)
        self.logger.warning(f"Your {self.__class__.__name__} class should have an __init__ method")
        raise NotImplementedError("You must override __init__")

    def _monitor_loop(self, *args, **kwargs):
        self.logger.warning(f"If you want to use your {self.__class__.__name__} class in a MonitorWindow, your Operator should have a _monitor_loop method")
        raise NotImplementedError("Must override _monitor_loop to use it")

    def load_config(self, filename, *args, **kwargs):
        self.logger.warning(f"Your {self.__class__.__name__} class should have a load_config method. Using method from OperatorBase")

        if not hasattr(self, 'properties'):
            self.logger.warning(f"Your {self.__class__.__name__} class does't have a properties dictionary yet: creating one")
            self.properties = {}
        if filename and not os.path.isfile(filename):
            self.logger.error('Config file not found: {}, falling back to default'.format(filename))
            return
        with open(filename, 'r') as f:
            self.properties.update(yaml.safe_load(f))
        self.properties['config_file'] = filename

    def do_scan(self, *args, **kwargs):
        self.logger.info("""
        do_scan is the default name for a scan method of an Operator. If you see this message that means you're trying to
        run do_scan() without having created it in your Operator. Note that you could use a different name, or create 
        multiple scan methods, but that you have to modify your GUI to actually  start those methods. 
        """)

    def save_scan(self, *args, **kwargs):
        self.logger.info("""
        save_scan is the default name for method of an Operator to save scan data. If you see this message that means 
        you're trying to call it (perhaps from a ScanWindow?) without having created it in your Operator. Note that you 
        could use a different name, or create multiple save methods (for multiple scans?), but that you have to modify 
        your GUI to actually use those save methods. 
        """)

    def disconnect_devices(self):
        self.logger.warning(f"Your {self.__class__.__name__} is missing the disconnect_devices method. Use that to disconnect from your devices when required.")

    # the next two methods are needed so the context manager 'with' works.
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """ This method get's called when exiting a python with block (when the code completed but also when an error occured)"""
        self.logger.debug('Calling disconnect_devices() before exiting with block')
        self.disconnect_devices()
