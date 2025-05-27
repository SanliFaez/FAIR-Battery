# -*- coding: utf-8 -*-
"""
=================
Basler controller
=================

BOTH THE FILE AND THE DOCUMENTATION ARE INCOMPLETE

"""

import time
#from threading import Event

from pypylon import pylon
import logging

from labphew.core.base.camera_base import BaseCamera

class BaslerCamera(BaseCamera):
    _acquisition_mode = BaseCamera.MODE_SINGLE_SHOT

    def __init__(self, camera):
        super().__init__(camera)
        self.logger = logging.getLogger(__name__)
        self.logger.debug('Creating BaslerCamera object')
        self.friendly_name = ''
        self.free_run_running = False
        #self._stop_free_run = Event()
        self.fps = 0


    def initialize(self):
        """ Initializes the communication with the camera. Get's the maximum and minimum width. It also forces
        the camera to work on Software Trigger.

        .. warning:: It may be useful to integrate other types of triggers in applications that need to
            synchronize with other hardware.

        """
        self.logger.debug('Initializing Basler Camera')
        tl_factory = pylon.TlFactory.GetInstance()
        devices = tl_factory.EnumerateDevices()
        if len(devices) == 0:
            #print('No camera found')
            self.logger.warning('No camera found')

        self._driver = None
        for device in devices:
            if self.cam_num in device.GetFriendlyName():
                self._driver = pylon.InstantCamera()
                self._driver.Attach(tl_factory.CreateDevice(device))
                self._driver.Open()
                self.friendly_name = device.GetFriendlyName()
            print(device.GetFriendlyName())

        if not self._driver:
            msg = f'Basler {self.cam_num} not found. Please check if the camera is connected'
            self.logger.error(msg)
            return

        # self.logger.info(f'Loaded camera {self._driver.GetDeviceInfo().GetModelName()}')

        # self._driver.RegisterConfiguration(pylon.SoftwareTriggerConfiguration(), pylon.RegistrationMode_ReplaceAll,
        #                                   pylon.Cleanup_Delete)

        #self.config.fetch_all()

    def __str__(self):
        if self.friendly_name:
            return f"Camera {self.friendly_name}"
        return super().__str__()

    def get_exposure(self):
        """ The exposure of the camera defined in microseconds """
        exposure = float(self._driver.ExposureTime)

        return exposure

    def set_exposure(self, exposure):
        """ The exposure of the camera is defined in microseconds """
        self.logger.info(f'Setting exposure to {exposure}')
        self._driver.ExposureTime.SetValue(exposure)

    def get_gain(self):
        """ Gain is a float """
        gain = float(self._driver.Gain.Value)
        return gain

    def set_gain(self, gain: float):
        self.logger.info(f'Setting gain to {gain}')
        self._driver.Gain.SetValue(gain)

    def get_acquisition_mode(self):
        return self._acquisition_mode

    def set_acquisition_mode(self, mode):
        # todo: this function requires careful adjustments to talk to Basler
        if self._driver.IsGrabbing():
            self.logger.warning(f'{self} Changing acquisition mode for a grabbing camera')

        #self.logger.info(f'{self} Setting acquisition mode to {mode}')
        if mode == self.MODE_CONTINUOUS:
            self.logger.debug(f'Setting buffer to {self._driver.MaxNumBuffer.Value}')
            self._acquisition_mode = mode
        elif mode == self.MODE_SINGLE_SHOT:
            self.logger.debug(f'Setting buffer to 1')
            self._acquisition_mode = mode

    def get_auto_exposure(self):
        """ Auto exposure can take one of three values: Off, Once, Continuous """
        return self._driver.ExposureAuto.Value

    def set_auto_exposure(self, mode: str):
        modes = ('Off', 'Once', 'Continuous')
        if mode not in modes:
            raise ValueError(f'Mode must be one of {modes} and not {mode}')
        self._driver.ExposureAuto.SetValue(mode)

    def get_auto_gain(self):
        """ Auto Gain must be one of three values: Off, Once, Continuous"""
        return self._driver.GainAuto.Value

    def set_auto_gain(self, mode):
        modes = ('Off', 'Once', 'Continuous')
        if mode not in modes:
            raise ValueError(f'Mode must be one of {modes} and not {mode}')
        self._driver.GainAuto.SetValue(mode)

    def get_pixel_format(self):
        """ Pixel format must be one of Mono8, Mono12, Mono12p"""
        return self._driver.PixelFormat.GetValue()

    def set_pixel_format(self, mode):
        """ Pixel format must be one of Mono8, Mono12, Mono12p"""

        self.logger.info(f'Setting pixel format to {mode}')
        self._driver.PixelFormat.SetValue(mode)

    def get_ROI(self):
        offset_X = self._driver.OffsetX.Value
        offset_Y = self._driver.OffsetY.Value
        width = self._driver.Width.Value - 1
        height = self._driver.Height.Value - 1
        return ((offset_X, offset_X+width),(offset_Y, offset_Y+height))

    def set_ROI(self, vals):
        X = vals[0]
        Y = vals[1]
        width = int(X[1] - X[1] % 4)
        x_pos = int(X[0] - X[0] % 4)
        height = int(Y[1] - Y[1] % 2)
        y_pos = int(Y[0] - Y[0] % 2)
        self.logger.info(f'Updating ROI: (x, y, width, height) = ({x_pos}, {y_pos}, {width}, {height})')
        self._driver.OffsetX.SetValue(0)
        self._driver.OffsetY.SetValue(0)
        self._driver.Width.SetValue(self.ccd_height)
        self._driver.Height.SetValue(self.ccd_height)
        self.logger.debug(f'Setting width to {width}')
        self._driver.Width.SetValue(width)
        self.logger.debug(f'Setting Height to {height}')
        self._driver.Height.SetValue(height)
        self.logger.debug(f'Setting X offset to {x_pos}')
        self._driver.OffsetX.SetValue(x_pos)
        self.logger.debug(f'Setting Y offset to {y_pos}')
        self._driver.OffsetY.SetValue(y_pos)
        self.X = (x_pos, x_pos + width)
        self.Y = (y_pos, y_pos + width)
        self.width = self._driver.Width.Value
        self.height = self._driver.Height.Value

    def get_ccd_height(self):
        return self._driver.Height.Max

    def get_ccd_width(self):
        return self._driver.Width.Max

    def trigger_camera(self):
        if self._driver.IsGrabbing():
            pass
            self.logger.warning('Triggering a grabbing camera')
        self._driver.StopGrabbing()
        mode = self.acquisition_mode
        if mode == self.MODE_CONTINUOUS:
            self._driver.StartGrabbing(pylon.GrabStrategy_OneByOne)
            self.logger.info('Grab Strategy: One by One')
        elif mode == self.MODE_SINGLE_SHOT:
            self._driver.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
            self.logger.info('Grab Strategy: Latest Image')
        elif mode == self.MODE_LAST:
            self._driver.StartGrabbing(pylon.GrabStrategy_LatestImages)
        self._driver.ExecuteSoftwareTrigger()
        self.logger.info('Executed Software Trigger')

    def read_camera(self) -> list:
        #todo: have to understand how the images are stored
        img = []
        mode = self.acquisition_mode
        if mode == self.MODE_SINGLE_SHOT or mode == self.MODE_LAST:
            self.logger.info(f'Grabbing mode: {mode}')
            grab = self._driver.RetrieveResult(int(self.exposure) + 100, pylon.TimeoutHandling_Return)
            if grab and grab.GrabSucceeded():
                img = [grab.GetArray().T]
                self.temp_image = img[0]
                grab.Release()
            if mode == self.MODE_SINGLE_SHOT:
                self._driver.StopGrabbing()
            return img
        else:
            if not self._driver.IsGrabbing():
                print('You need to trigger the camera before reading')
            num_buffers = self._driver.NumReadyBuffers.Value
            if num_buffers:
                img = [None] * num_buffers
                for i in range(num_buffers):
                    grab = self._driver.RetrieveResult(int(self.exposure) + 100, pylon.TimeoutHandling_ThrowException)
                    if grab and grab.GrabSucceeded():
                        img[i] = grab.GetArray().T
                        grab.Release()
                img = [i for i in img if i is not None]
        if len(img) >= 1:
            self.temp_image = img[-1]
        return img

    def get_frame_asarray(img):
        # todo : to convert a single readout frame to an array of correct format
        pass

    def start_free_run(self):
        """ Starts a free run from the camera. It will preserve only the latest image. It depends
        on how quickly the experiment reads from the camera whether all the images will be available
        or only some.
        """
        if self.free_run_running:
            self.logger.info(f'Trying to start again the free acquisition of camera {self}')
            return
        self.logger.info(f'Starting a free run acquisition of camera {self}')
        self.free_run_running = True
        self.logger.debug('First frame of a free_run')
        self.acquisition_mode = self.MODE_CONTINUOUS
        self.trigger_camera()  # Triggers the camera only once

    def stop_free_run(self):
        self._stop_free_run.set()

    def stop_camera(self):
        self._driver.StopGrabbing()

    def finalize(self):
        self.stop_free_run()
        self.stop_camera()
        #self.clean_up_threads()
        #super().finalize()


if __name__ == '__main__':

    logging.basicConfig(level=logging.DEBUG)  # This allows logging comments of levels DEBUG and above (i.e. all levels)
    # Change this to INFO or WARNING to see less logging prints.

    cam = BaslerCamera('da')
    cam.initialize()
    Nx , Ny = cam.get_ccd_width(), cam.get_ccd_height()
    print("chip size:", Nx, Ny)
    mode = cam.get_acquisition_mode()
    cam.start_free_run()
    time.sleep(1)
    for i in range(1):
        frame = cam.read_camera()
        print(frame)
    cam.stop_camera()