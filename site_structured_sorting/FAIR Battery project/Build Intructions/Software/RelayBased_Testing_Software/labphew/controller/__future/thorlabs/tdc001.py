import ctypes
import ctypes.util
from ctypes.wintypes import DWORD, WORD

from lantz import Driver
from lantz import Feat, Action
from lantz import Q_

from .data_types import MOT_DC_PIDParameters, TLI_HardwareInformation, MOT_HomingParameters, \
    MOT_JogParameters


class TDC(Driver):
    LIBRARY_NAME = 'Thorlabs.MotionControl.TCube.DCServo.DLL'

    def __init__(self, serial, *args, **kwargs):
        super().__init__(*args, **kwargs)
        filename = ctypes.util.find_library(self.LIBRARY_NAME)
        try:
            self.lib = ctypes.cdll.LoadLibrary(filename)
        except:
            raise Exception('ERROR')
        if not isinstance(serial, str):
            serial = str(serial)
        self.serial = serial.encode('utf-8')
        self.lib.CC_Open(self.serial)
        self.lib.CC_LoadSettings(self.serial)
        self.lib.CC_StartPolling(self.serial, ctypes.c_int(500))
        self.num_position = self.lib.CC_GetNumberPositions(self.serial)


    @Feat()
    def can_home(self):
        return bool(self.lib.CC_CanHome(self.serial))

    @Feat()
    def can_move_without_home(self):
        return bool(self.lib.CC_CanMoveWithoutHomingFirst(self.serial))

    @Feat()
    def check_connection(self):
        return bool(self.lib.CC_CheckConnection(self.serial))

    @Feat(units='deg')
    def position(self):
        # In device units
        dev_position = self.lib.CC_GetPosition(self.serial)
        return dev_position/self.num_position*360*Q_('deg')

    @position.setter
    def position(self, value):
        dev_position = int(value/360*self.num_position)
        dev_position = ctypes.c_int(dev_position)
        self.lib.CC_MoveToPosition(self.serial, dev_position)

    @Action()
    def clear_message_queue(self):
        self.lib.CC_ClearMessageQueue(self.serial)

    @Action()
    def close(self):
        self.lib.CC_Close(self.serial)

    @Action()
    def disable_channel(self):
        self.lib.CC_DisableChannel(self.serial)

    @Action()
    def enable_channel(self):
        self.lib.CC_EnableChannel(self.serial)

    def enable_last_msg_timer(self, timeout=0):
        """ Enables the last message monitoring timer.
        :param timeout: Timeout time in milliseconds.
        """
        enable = ctypes.c_bool(True)
        timeout = ctypes.c_int32(timeout)
        self.lib.CC_EnableLastMsgTimer(self.serial, enable, timeout)

    @Feat()
    def backlash(self):
        return self.lib.CC_GetBacklash(self.serial)

    def get_DCPID_params(self):
        params = MOT_DC_PIDParameters()
        self.lib.CC_GetDCPIDParams(self.serial, ctypes.byref(params))
        return params

    def get_hardware_info(self):
        info = TLI_HardwareInformation()
        self.lib.CC_GetHardwareInfoBlock(self.serial, ctypes.byref(info))
        return info

    def get_homing_parameters(self):
        params = MOT_HomingParameters()
        self.lib.CC_GetHomingParamsBlock(self.serial, ctypes.byref(params))
        return params

    def get_homing_velocity(self):
        return self.lib.CC_GetHomingVelocity(self.serial)

    def get_jog_mode(self):
        mode = ctypes.c_int64()
        stop_modes = ctypes.c_int64()
        self.lib.CC_GetJogMode(self.serial, ctypes.byref(mode), ctypes.byref(stop_modes))
        return mode, stop_modes

    def get_jog_parameters(self):
        params = MOT_JogParameters()
        self.lib.CC_GetJogParamsBlock(self.serial, ctypes.byref(params))
        return params

    def get_jog_step_size(self):
        return self.lib.CC_GetJogStepSize(self.serial)

    def get_jog_vel_params(self):
        acceleration = ctypes.c_int()
        maxVelocity = ctypes.c_int()
        self.lib.CC_GetJogVelParams(self.serial, ctypes.byref(acceleration), ctypes.byref(maxVelocity))
        return acceleration, maxVelocity

    def get_led_switches(self):
        """ Get the LED indicator bits on cube.
        :return: Sum of: 8 to indicate moving 2 to indicate end of track and 1 to flash on identify command.
        """
        return self.lib.CC_GetLEDswitches(self.serial)

    def get_next_message(self):
        messageType = WORD()
        messageID = WORD()
        messageData = DWORD()
        self.lib.CC_GetNextMessage(self.serial, ctypes.byref(messageType), ctypes.byref(messageID), ctypes.byref(messageData))
        return messageType, messageID, messageData

    @Action()
    def home_device(self):
        self.lib.CC_Home(self.serial)


if __name__ == '__main__':
    import os
    import time
    os.environ['PATH'] = os.environ['PATH'] + ';' + 'C:\\Program Files (x86)\\Thorlabs\\Kinesis'
    with TDC011("83843619") as inst:
        inst.enable_channel()
        print('Position: {}'.format(inst.position))
        new_pos = 102*Q_('deg')
        # inst.position = new_pos
        time.sleep(1)
        inst.lib.CC_Home(inst.serial)
        while True:
            # mt, mi, md = inst.get_next_message()
            # print('Message Type: {}'.format(mt))
            # print('Message ID: {}'.format(mi))
            # print('Message Data: {}'.format(md))
            print(inst.position)
            time.sleep(1)