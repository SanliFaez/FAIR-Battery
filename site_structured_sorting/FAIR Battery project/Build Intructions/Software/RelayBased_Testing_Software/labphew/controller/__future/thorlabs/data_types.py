"""
    thorlabs_data_types
    ===================
    Defines the data structures needed for the devices used by Kinesis. They are broadly documented in
    the Kinesis installation folder, file Thorlabs.MotionControl.C_API.chm.
"""

import ctypes.util
from ctypes.wintypes import DWORD, WORD

class TLI_DeviceInfo(ctypes.Structure):
    """ Device info."""
    _fields_ = [('typeID', DWORD),
        ('description', ctypes.c_char*65), #type(ctypes.create_string_buffer(65))),
        ('serialNo', ctypes.c_char*9), #type(ctypes.create_string_buffer(9))),
        ('PID', DWORD),
        ('isKnownType', ctypes.c_bool),
        ('motorType', ctypes.c_int64),
        ('isPiezoDevice', ctypes.c_bool),
        ('isLaser', ctypes.c_bool),
        ('isCustomType', ctypes.c_bool),
        ('isRack', ctypes.c_bool),
        ('maxChannels', ctypes.c_short)]

class TLI_HardwareInformation(ctypes.Structure):
    _fields_ = [('serialNumber', DWORD),
                ('modelNumber', ctypes.c_char*8),
                ('type', WORD),
                ('numChannels', ctypes.c_short),
                ('notes', ctypes.c_char*48),
                ('firmwareVersion', DWORD),
                ('hardwareVersion', WORD),
                ('deviceDependantData', ctypes.c_byte*12),
                ('modificationState', WORD)]

class MOT_VelocityParameters(ctypes.Structure):
    _fields_ = [('minVelocity', ctypes.c_int),
                ('acceleration', ctypes.c_int),
                ('maxVelocity', ctypes.c_int)]

class MOT_JogParameters(ctypes.Structure):
    _fields_ = [('mode', ctypes.c_short),
                ('stepSize', ctypes.c_uint),
                ('velParams', MOT_VelocityParameters),
                ('stopMode', ctypes.c_short)]

class MOT_HomingParameters(ctypes.Structure):
    _fields_ = [('direction', ctypes.c_short),
                ('limitSwitch', ctypes.c_short),
                ('velocity', ctypes.c_uint),
                ('offsetDistance', ctypes.c_uint)]

class MOT_LimitSwitchParameters(ctypes.Structure):
    _fields_ = [('clockwiseHardwareLimit', WORD),
                ('anticlockwiseHardwareLimit', WORD),
                ('clockwisePosition', DWORD),
                ('anticlockwisePosition', DWORD),
                ('softLimitMode', WORD)]

class MOT_ButtonParameters(ctypes.Structure):
    _fields_ = [('buttonMode', WORD),
                ('leftButtonPosition', ctypes.c_int),
                ('rightButtonPosition', ctypes.c_int),
                ('timeout', WORD),
                ('unused', WORD)]

class MOT_PotentiometerStep(ctypes.Structure):
    _fields_ = [('thresholdDeflection', WORD),
                ('velocity', DWORD)]

class MOT_PotentiometerSteps(ctypes.Structure):
    _fields_ = [('potentiometerStepParameters', 4*MOT_PotentiometerStep)]

class MOT_DC_PIDParameters(ctypes.Structure):
    _fields_ = [('proportionalGain', ctypes.c_int),
                ('integralGain', ctypes.c_int),
                ('differentialGain', ctypes.c_int),
                ('integralLimit', ctypes.c_int),
                ('parameterFilter', WORD)]