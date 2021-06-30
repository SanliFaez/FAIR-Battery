"""
Start Function
==============
After installing labphew it is possible to start it directly from within the command line using `labphew start`.
It takes two arguments that is the name of the example and a path to the configuration file.

    $ labphew start blink -default

"""
import sys
import labphew
import os
import glob
# from PyQt5.QtWidgets import QApplication, QFileDialog
# from time import time

def main():
    """Starts the GUI for the application using the config file specified as system argument.
    """

    # note: 0th argument will be labphew

    if len(sys.argv) < 3 or sys.argv[1] != 'start':
        show_help()
        return

    # # if no additional argument (i.e. config file) was given, show open file dialog:
    # if len(sys.argv) < 4:
    #     app = QApplication([])
    #     ofdlg = QFileDialog()
    #     config_file = ofdlg.getOpenFileName(None, 'Open config file', filter = "YAML (*.yml);;All Files (*.*)")
    #     ofdlg.close()
    #     del app
    #     if config_file[0]:
    #         sys.argv.append(config_file[0])

    try:
        labphew.start(*sys.argv[2:])
    except:
        return

def show_help():
    yml_path = os.path.join(labphew.repository_path, 'examples', 'default_config', 'blink_config.yml')
    print('\n'+help_message.format(yml_path))
    print("These appear to be possible examples:")
    for fi in [os.path.basename(f) for f in glob.glob(labphew.package_path + '/*.py')]:
        if not fi.startswith('__'):
            print('  ' + os.path.splitext(fi)[0])
    print('')

help_message = \
"""
Congratulations! 
You're almost ready to run your labphew module
----------------------------------------------
In order to run a module with labphew, you need to insert the module name (and optionally the path to the config file). 
For example, you can invoke this program as:
labphew start blink {}

For blink (and other files where it's implemented) you could use -default or -d for the config file
and -browse or -b to open a browse window.
"""

if __name__ == "__main__":
    main()
