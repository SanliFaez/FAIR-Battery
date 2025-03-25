"""
Example start file
==================

Run this file from an interactive python console, or from command line:
  >>> python start.py my_blink_config.yml
Note that both arguments need to point to the files in this folder, so this example command assumes you are already in
the directorycontaining this example.
"""

import sys
import labphew
from labphew.core.tools.gui_tools import open_config_dialog
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
import os
import Battery_Testing_Software

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Optionally place the path to your default config file here:
default_config = os.path.join(Battery_Testing_Software.package_path, 'examples', 'my_blink_project',
                              'my_blink_config.yml')

# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<


def main(config_file=default_config):
    """
    Starts the GUI of the Blink example.
    Note, if config_file is not specified, or is set to '-default' or '-d', it will fall back to a default file
    specified in this module.
    Note, if '-browse' or '-b' is used for config_file, it will display a window that allows you to browse to the file.
    Note, if no config_file is specified, load_config() of the operator wil be called without config filename.

    :param config_file: optional path to config file
    :type config_file: str
    """

    # If -browse (or -b) is used for config_file, display an open file dialog:
    if config_file == '-browse' or config_file == '-b':
        config_file = open_config_dialog()
    # If -default (or -d) is used for config_file, switch it out for the default specified in the top of this file:
    if config_file == '-default' or config_file == '-d':
        config_file = default_config
        print('Using default_config file specified in {}'.format(__name__))
    if config_file is None:
        print('Using Operator without specifying a config file.')

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # Load your classes and create your gui:

    from my_blink_controller import BlinkController
    from my_blink_model import BlinkOperator
    from my_blink_view import MonitorWindow, ScanWindow

    instr = BlinkController()
    opr = BlinkOperator(instr)

    opr.load_config(config_file)

    # Create a PyQt application:
    app = QApplication([])
    app_icon = QIcon(os.path.join(labphew.package_path, 'view', 'design', 'icons', 'labphew_icon.png'))
    app.setWindowIcon(app_icon)  # set an icon
    # Gui elements created now will be part of the PyQt application

    main_gui = MonitorWindow(opr)

    scan_gui = ScanWindow(opr, parent=main_gui)
    # fit_on_screen(scan_window)
    scans = {
        'Example scan 1': scan_gui
    }
    main_gui.load_scan_guis(scans)
    main_gui.show()

    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

    # This line will start the application:
    error_code = app.exec_()
    sys.exit(error_code)


if __name__ == '__main__':
    # When run from command line, this code will pass the command line argument as an argument in the main() function
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main()
