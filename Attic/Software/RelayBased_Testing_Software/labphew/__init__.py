"""
Labphew
=======

Fun with computer-controlled experiments for beginners.

More documentation can be found on `Read the Docs <https://labphew.readthedocs.io>`_.
The repository can be found on `Github <https://github.com/SanliFaez/labphew>`_.

To quickly test if it works try this from command line:
  >>> labphew start blink -default
Or from an interactive python console:
  >>> import labphew
  >>> labphew.start.blink('-default')

"""

# Get the version from the package setup.py file
from pkg_resources import get_distribution
try:
    __version__ = get_distribution("labphew").version
except:
    __version__ = "unknown"

import os
package_path = os.path.dirname(os.path.abspath(__file__))
repository_path = os.path.abspath(os.path.join(package_path, os.pardir))
parent_path = os.path.abspath(os.path.join(repository_path, os.pardir))

from pint import UnitRegistry
ureg = UnitRegistry()
Q_ = ureg.Quantity

import logging
# Set standard logging format and level.
# (To use this, do 'import labphew' in your module)
logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s] %(levelname)-8s: %(message)-50s  [%(lineno)d %(name)s]",
    datefmt='%H:%M:%S')

# Matplotlib uses the default logger and by setting the level to DEBUG in basicConfig, matplotlib will print a lot of
# debug statements. We prevent that by the logger used by matplotlib manually to level WARNING
logging.getLogger('matplotlib').setLevel(logging.WARNING)

from importlib import import_module
class _Start:
    """
    Calls the main() function of a module in the root of the package.
    The name of the module may be passed as the first argument, or accessed as an attribute.

    Example usages:
    >>> labphew.start('blink', 'optional_config_file_name.yml')
    >>> labphew.start.blink('optional_config_file_name.yml')

    """
    def __init__(self):
        self.__modules = {}

        for file in os.listdir(package_path):
            if file.endswith('.py') and not file.startswith('__'):
                self.add_module_main(file[:-3])

    def add_module_main(self, name):
        try:
            mod = import_module('labphew.'+name)
            self.__setattr__(name, getattr(mod, 'main'))
            self.__modules[name] = getattr(mod, 'main')
        except:
            return

    def __getattr__(self, name):
        print('ERROR: Module {}.py does was not found or failed to import'.format(name))

    def __call__(self, *args, **kwargs):
        if len(args) < 1:
            print('ERROR')
            return
        return self.__getattribute__(args[0])(*args[1:])

start = _Start()
