"""
GUI Tools
=========

Collection of tools that might be helpful for GUIs

"""
import logging
import labphew
import numpy as np
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import os.path
import yaml
import pyqtgraph as pg
from time import time

def set_spinbox_stepsize(spinbox):
    """ Helper function that sets the stepsize of a spinbox to one order of magnitude below current value. """
    if type(spinbox) is QDoubleSpinBox:
        min_pow = - spinbox.decimals()
    elif type(spinbox) is QSpinBox:
        min_pow = 0
    else:
        return
    if spinbox.value() == 0:
        p = min_pow
    else:
        p = max(min_pow, int(np.floor(np.log10(np.abs(spinbox.value()))))-1)
    spinbox.setSingleStep(10 ** p)


class SaverWidget(QWidget):
    """
    Simple widget for saving, consisting of a line edit to enter the filename and a save button.
    It overwrites existing files without confirmation, but the line edit turns red to warn the user that the file exists.
    In addition it has the option to save through a browse window.
    And it has the option to store the entire properties dictionary in a yaml file (of the same name).
    """
    def __init__(self, save_button_callback):
        """
        Create the saver widget. The saving method (of the operator) needs to be passed as argument.

        :param save_button_callback: the saving method to call
        :type save_button_callback: method
        """
        super().__init__()
        self.__save_button_callback = save_button_callback
        self.setLayout(QVBoxLayout())
        top_layout = QHBoxLayout()
        bottom_layout = QHBoxLayout()
        self.layout().addLayout(top_layout)
        self.layout().addLayout(bottom_layout)

        self.filename = QLineEdit(r'C:\Temp\data.nc')
        self.filename.textChanged.connect(self.check_file_exists)
        self.check_file_exists()
        self.browse_button = QPushButton('Browse')
        self.browse_button.clicked.connect(self.browse)

        self.save_button = QPushButton('Save')
        self.save_button.clicked.connect(self.save)
        self.conf_checkbox = QCheckBox('Store config', checked=True, statusTip='Stores the current operator properties into a yaml config file of the same name')

        top_layout.addWidget(self.filename)
        top_layout.addWidget(self.browse_button)
        bottom_layout.addWidget(self.conf_checkbox)
        bottom_layout.addWidget(self.save_button)


    def save(self):
        """ Calls the saving method (of operator) and then calls check_file_exists to turn the filename red."""
        self.__save_button_callback(self.filename.text(), store_conf=self.conf_checkbox.isChecked())
        self.check_file_exists()

    def check_file_exists(self):
        """ Makes the filename line edit red if file exists, or black otherwise."""
        if os.path.exists(self.filename.text()):
            self.filename.setStyleSheet("color: red;")
        else:
            self.filename.setStyleSheet("color: black;")

    def browse(self):
        if os.path.isdir(os.path.dirname(self.filename.text())):
            fname = self.filename.text()
        else:
            fname = os.path.join(labphew.parent_path, 'data.nc')
        fname = QFileDialog.getSaveFileName(self, 'Save data as', fname,
                                                filter="netCDF4 (*.nc);;All Files (*.*)")
        self.__save_button_callback(fname[0], store_conf=self.conf_checkbox.isChecked())
        self.filename.setText(fname[0])


class ModifyConfig(QDialog):
    """
    Window to modify any dictionary as if it were yaml text.
    Note that for a gui it is useful to update the gui elements affected by the changes. For that purpose the parent gui
    can pass an update method to this window through apply_callback.
    """

    def __init__(self, properties_dict, apply_callback=None, parent=None):
        """
        Create the Modify Config window.

        :param properties_dict: dictionary to be modified
        :type properties_dict: dict
        :param apply_callback: optional method to be called by apply button after updating the dictionary
        :type apply_callback: method (or None)
        :param parent: The parent window
        :type parent: QtWidget


        """
        self.logger = logging.getLogger(__name__)
        self.logger.debug('Creating Modify Config window')
        super().__init__(parent=parent)
        self._parent = parent
        self.setWindowTitle('Modify properties with yaml code')
        self.apply_callback = apply_callback
        # self.apply_props = apply
        self.font = QFont("Courier New", 11)
        self.properties_dict = properties_dict
        self.initUI()
        self.reset_text()
        self.set_size()

    def initUI(self):
        """Create the GUI layout"""
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        main_layout = QVBoxLayout()
        button_layout = QHBoxLayout()
        # create buttons, labels and the textedit:
        self.button_apply = QPushButton('&Apply', clicked=self.apply)
        self.button_reset = QPushButton('&Reset', clicked = self.reset_text)
        self.button_cancel = QPushButton('&Cancel', clicked = self.close)

        self.txt = QTextEdit()
        self.txt.setLineWrapMode(QTextEdit.NoWrap)
        self.txt.setFont(self.font)
        self.txt.textChanged.connect(self.changed)

        button_layout.addWidget(self.button_apply)
        button_layout.addWidget(self.button_reset)
        button_layout.addWidget(self.button_cancel)
        main_layout.addWidget(self.txt)
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

    def set_size(self):
        # Adjust window size to text (if possible)
        # These values were chosen in Windows 7
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        font_metrics = QFontMetrics(self.font)
        max_width = min(QDesktopWidget().availableGeometry(self).width(), QDesktopWidget().screenGeometry(self).width())
        max_height = min(QDesktopWidget().availableGeometry(self).height(), QDesktopWidget().screenGeometry(self).height())
        width = max(400, min(max_width-16, self.txt.document().idealWidth() + 42+10))
        height = max(400, min(max_height-38, font_metrics.size(0, self.txt.toPlainText()).height() + 145))
        self.resize(width, height)

    def changed(self):
        """
        Sets the correct enabled state of buttons after the text field has changed. (Is called after every change).

        Note:
        It also checks if the yaml is valid after every change (and sets button state accordingly). If that turns out to
        be too intensive, there's a suggestion for modification in the source code.
        """
        self.button_reset.setEnabled(True)
        self.button_apply.setEnabled(self.valid_yaml())
        # It might be a bit intensive to continuously check if the whole text is valid yaml.
        # If that turns out to be the case, just change it to:
        # self.button_apply.setEnabled(True)

    def reset_text(self):
        """Called by reset button. Resets the text field to the original dictionary and resets the buttons accordingly."""
        self.txt.setText(yaml.dump(self.properties_dict))
        self.button_reset.setEnabled(False)
        self.button_apply.setEnabled(False)

    def valid_yaml(self, quiet=True):
        """
        Checks if text in input field can be interpreted as valid yaml.
        Returns True for valid yaml, False otherwise
        If optional keyword quiet is set to False it will also display a warning pop-up.

        :param quiet: flag to suppress the warning pop-up (default: True)
        :type quiet: bool
        :return: yaml validity
        :rtype: bool
        """
        try:
            self._list = yaml.safe_load(self.txt.toPlainText())
            return True
        except yaml.YAMLError as exc:
            if not quiet:
                QMessageBox.warning(self, 'Invalid YAML', str(exc), QMessageBox.Ok)
            return False

    def apply(self):
        """
        Called by apply button.
        Converts the text window to dictionary (using yaml) and updates the original dictionary.
        If a apply_callback was supplied it will attempt to execute it.
        """
        if self.valid_yaml(False):
            try:
                # self.logger.debug('Converting text to dictionary')
                dic = yaml.safe_load(self.txt.toPlainText())
                if type(dic) is not dict:
                    raise
            except:
                self.logger.error('Converting text to dictionary failed')
                QMessageBox.warning(self, 'Reading YAML failed', 'Error while converting yaml to dictionary', QMessageBox.Ok)
                return
            self.properties_dict.update(dic)
            if self.apply_callback is not None:
                try:
                    self.apply_callback()
                except:
                    self.logger.error('Apply callback caused unexpected exception')
                    QMessageBox.warning(self, 'Error', 'Apply callback caused unexpected exception', QMessageBox.Ok)
                    return
            self.close()


def open_config_dialog(optional_path=None):
    """
    Displays an Open file dialog window, to open a yaml config file.
    It returns the path to the file or '-default'  if window closed/cancelled
    An optional argument may be passed to indicate the path where to start the browse window. If omitted the default
    location for PyQt QFileDialog.getOpenFileName will be used.

    :param optional_path: optional path where to start the open dialog
    :type optional_path: str
    :return: path to the file (or '-default' if window closed/cancelled)
    :rtype: str
    """
    app = QApplication([])
    ofdlg = QFileDialog()
    config_file = ofdlg.getOpenFileName(None, 'Open config file', directory=optional_path, filter = "YAML (*.yml);;All Files (*.*)")
    ofdlg.close()
    del app
    if config_file[0]:
        return config_file[0]
    else:
        return '-default'


class ValueLabelItem(pg.LabelItem):
    """
    Convenience class that combines functionality of pyqtgraph.ValueLabel() into a pyqtgraph.LabelItem().
    It inherits from LabelItem and thus may be used in the same manner. But it adds the a setValue() method of
    ValueLabel and it also accepts the keyword arguments of ValueLabel.
    Additionally, the precision may be modified (with siPrecision) when using siPrefix mode.
    Additionally, the rate at which the text is updated may be controlled through textUpdateTime.
    Additionally, any method unknown to LabelItem will be passed to the internal ValueLabel object.
    """
    def __init__(self, text='', parent=None, suffix='', siPrefix=False, averageTime=0, formatStr=None, siPrecision=3, textUpdateTime=None, **kwargs):
        """
        Convenience class that combines pyqtgraph.ValueLabel into a pyqtgraph.LabelItem.
        It inherits from LabelItem so see that documentation for usage and arguments.
        It adds the setValue method of ValueLabel. All other unknown methods are passed on to the internal ValueLabel
        object.
        The ValueLabel arguments are passed on to the internal ValueLabel object.
        It has two additional arguments. siPrecision allows to modify the number of significant digits while the
        ValueLabel has siPrefix=True. textUpdateTime allows to reduce the frequency of updating the gui by not updating
        the text every call to setValue (default value of None, does update every time)
        Note that the arguments of LabelItem are not included in this docstring (except for text), please refer to
        LabelItem documentation.

        :param text: initial text to display (see pyqtgraph.LabelItem)
        :type text: str
        :param suffix: the (SI) unit
        :type suffix: str
        :param siPrefix: when True it converts things like 0.024 V to 24 mV
        :type siPrefix: bool
        :param averageTime: optional, see pyqtgraph.ValueLabel
        :type averageTime: float
        :param formatStr: optional, see pyqtgraph.ValueLabel
        :type formatStr: str
        :param siPrecision: optional, allows to deviate from the default of 3 significant digits
        :type siPrecision: int
        :param textUpdateTime: optional, time between updates of text (default is None which updates every time)
        :type textUpdateTime: float
        """
        value_kwargs = {'parent':parent}
        if suffix is not None:
            value_kwargs['suffix'] = suffix
        if siPrefix is not None:
            value_kwargs['siPrefix'] = siPrefix
        if averageTime is not None:
            value_kwargs['averageTime'] = averageTime
        if formatStr is not None:
            value_kwargs['formatStr'] = formatStr
        super().__init__(text=text, parent=parent, **kwargs)
        self._ValueLabel = pg.ValueLabel(**value_kwargs)
        self.__siPrecision = siPrecision
        self.__textUpdateTime = textUpdateTime
        self.__last_update_text = time()

    def setValue(self, value):
        self._ValueLabel.setValue(value)
        if self.__textUpdateTime is None or time() > self.__last_update_text + self.__textUpdateTime:
            self.__last_update_text = time()
            if self._ValueLabel.siPrefix:
                self.setText(pg.functions.siFormat(self._ValueLabel.averageValue(), self.__siPrecision, suffix=self._ValueLabel.suffix))
            else:
                self.setText(self._ValueLabel.generateText())

    def __getattr__(self, item):
        return getattr(self._ValueLabel, item)

def fit_on_screen(self):
    """Function to move and resize a QMainWindow (or maybe any QWidget) to fit on the available space of the current desktop screen."""
    frameGm = self.frameGeometry()
    screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
    availGm = QApplication.desktop().availableGeometry(screen)
    # reduce size if larger than available desktop area
    if frameGm.height() > availGm.height():
        frameGm.setHeight(availGm.height())
    if frameGm.width() > availGm.width():
        frameGm.setWidth(availGm.width())
    # move if any side is outside available desktop area
    if frameGm.top() < availGm.top():
        frameGm.moveTop(availGm.top())
    if frameGm.bottom() > availGm.bottom():
        frameGm.moveBottom(availGm.bottom())
    if frameGm.left() < availGm.left():
        frameGm.moveLeft(availGm.left())
    if frameGm.right() > availGm.right():
        frameGm.moveRight(availGm.right())
    self.setGeometry(frameGm)
