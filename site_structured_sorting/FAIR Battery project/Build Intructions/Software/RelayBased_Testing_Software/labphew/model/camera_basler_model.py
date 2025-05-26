"""
    Basler Camera Model
    ===================
    Model to adapt PyPylon to the needs of PyNTA. PyPylon is only a wrapper for Pylon, thus the documentation
    has to be found in the folder where Pylon was installed. It refers only to the C++ documentation, which is
    very extensive, but not necessarily clear.

    Some assumptions
    ----------------
    The program forces software trigger during :meth:`~labphew.model.camera_basler_model.initialize`.
"""
import logging
import warnings
from typing import Tuple
from pypylon import pylon

from experimentor import Q_
from experimentor.lib.log import get_logger
from experimentor.models.cameras.base_camera import BaseCamera
from experimentor.models.cameras.exceptions import CameraNotFound, WrongCameraState, CameraException

logger = get_logger(__name__)


class Camera(BaseCamera):
    def __init__(self, camera):
        super().__init__(camera)
        self.cam_num = camera
        self.max_width = 0
        self.max_height = 0
        self.width = None
        self.height = None
        self.mode = None
        self.X = None
        self.Y = None
        self.friendly_name = None

    def initialize(self):
        """ Initializes the communication with the camera. Get's the maximum and minimum width. It also forces
        the camera to work on Software Trigger.

        .. warning:: It may be useful to integrate other types of triggers in applications that need to
            synchronize with other hardware.

        """
        logger.debug('Initializing Basler Camera')
        tl_factory = pylon.TlFactory.GetInstance()
        devices = tl_factory.EnumerateDevices()
        if len(devices) == 0:
            raise CameraNotFound('No camera found')

        for device in devices:
            if self.cam_num in device.GetFriendlyName():
                self.camera = pylon.InstantCamera()
                self.camera.Attach(tl_factory.CreateDevice(device))
                self.camera.Open()
                self.friendly_name = device.GetFriendlyName()

        if not self.camera:
            msg = f'{self.cam_num} not found. Please check your config file and cameras connected'
            logger.error(msg)
            raise CameraNotFound(msg)

        logger.info(f'Loaded camera {self.camera.GetDeviceInfo().GetModelName()}')

        self.max_width = self.camera.Width.Max
        self.max_height = self.camera.Height.Max
        offsetX = self.camera.OffsetX.Value
        offsetY = self.camera.OffsetY.Value
        width = self.camera.Width.Value
        height = self.camera.Height.Value
        self.X = (offsetX, offsetX+width)
        self.Y = (offsetY, offsetY+height)

        self.camera.RegisterConfiguration(pylon.SoftwareTriggerConfiguration(), pylon.RegistrationMode_ReplaceAll,
                                          pylon.Cleanup_Delete)
        self.set_acquisition_mode(self.MODE_SINGLE_SHOT)
        self.get_size()
        self.get_exposure()

    def set_acquisition_mode(self, mode):
        logger.info(f'Setting acquisition mode to {mode}')
        if mode == self.MODE_CONTINUOUS:
            logger.debug(f'Setting buffer to {self.camera.MaxNumBuffer.Value}')
            self.camera.OutputQueueSize = self.camera.MaxNumBuffer.Value
            self.camera.AcquisitionMode.SetValue('Continuous')
            self.mode = mode
        elif mode == self.MODE_SINGLE_SHOT:
            self.camera.AcquisitionMode.SetValue('SingleFrame')
            self.mode = mode

        self.camera.AcquisitionStart.Execute()

    def set_ROI(self, X: Tuple[int, int], Y: Tuple[int, int]) -> Tuple[int, int]:
        """ Set up the region of interest of the camera. Basler calls this the
        Area of Interest (AOI) in their manuals. Beware that not all cameras allow
        to set the ROI (especially if they are not area sensors).
        Both the corner positions and the width/height need to be multiple of 4.
        Compared to Hamamatsu, Baslers provides a very descriptive error warning.

        :param tuple X: Horizontal limits for the pixels, 0-indexed and including the extremes. You can also check
            :mod:`Base Camera <pynta.model.cameras.base_camera>`
            To select, for example, the first 100 horizontal pixels, you would supply the following: (0, 99)
        :param tuple Y: Vertical limits for the pixels.

        """
        width = abs(X[1]-X[0])+1
        width = int(width-width%4)
        x_pos = int(X[0]-X[0]%4)
        height = int(abs(Y[1]-Y[0])+1)
        y_pos = int(Y[0]-Y[0]%2)
        logger.info(f'Updating ROI: (x, y, width, height) = ({x_pos}, {y_pos}, {width}, {height})')
        if x_pos+width > self.max_width:
            raise CameraException('ROI width bigger than camera area')
        if y_pos+height > self.max_height:
            raise CameraException('ROI height bigger than camera area')

        # First set offset to minimum, to avoid problems when going to a bigger size
        self.clear_ROI()
        logger.debug(f'Setting width to {width}')
        self.camera.Width.SetValue(width)
        logger.debug(f'Setting X offset to {x_pos}')
        self.camera.OffsetX.SetValue(x_pos)
        logger.debug(f'Setting Height to {height}')
        self.camera.Height.SetValue(height)
        logger.debug(f'Setting Y offset to {y_pos}')
        self.camera.OffsetY.SetValue(y_pos)
        self.X = (x_pos, x_pos+width)
        self.Y = (y_pos, y_pos+width)
        self.width = self.camera.Width.Value
        self.height = self.camera.Height.Value
        return self.width, self.height

    def clear_ROI(self):
        """ Resets the ROI to the maximum area of the camera"""
        self.camera.OffsetX.SetValue(self.camera.OffsetX.Min)
        self.camera.OffsetY.SetValue(self.camera.OffsetY.Min)
        self.camera.Width.SetValue(self.camera.Width.Max)
        self.camera.Height.SetValue(self.camera.Height.Max)

    def GetCCDWidth(self) -> int:
        """ Get the full width of the camera sensor.

        :return int: Maximum width

        .. deprecated:: 0.1.3
           Use self.max_width instead

        """
        warnings.warn("This method will be removed in a future release. Use cls.max_width instead", DeprecationWarning)
        return self.max_width

    def GetCCDHeight(self) -> int:
        """ Get the full height (in pixels) of the camera sensor.

        :return int: Maximum height

        .. deprecated:: 0.1.3
            Use self.max_height instead

        """
        warnings.warn("This method will be removed in a future release. Use cls.max_height instead", DeprecationWarning)
        return self.max_height

    def get_size(self) -> Tuple[int, int]:
        """ Get the size of the current Region of Interest (ROI). Remember that the actual size may be different from
        the size that the user requests, given that not all cameras accept any pixel. For example, Basler has some
        restrictions regarding corner pixels and possible widths.

        :return tuple: (Width, Height)
        """
        return self.camera.Width.Value, self.camera.Height.Value

    def trigger_camera(self):
        if self.camera.IsGrabbing():
            logger.warning('Triggering an already grabbing camera')
        else:
            if self.mode == self.MODE_CONTINUOUS:
                self.camera.StartGrabbing(pylon.GrabStrategy_OneByOne)
            elif self.mode == self.MODE_SINGLE_SHOT:
                self.camera.StartGrabbing(1)
        self.camera.ExecuteSoftwareTrigger()

    def set_exposure(self, exposure: Q_) -> Q_:
        self.camera.ExposureTime.SetValue(exposure.m_as('us'))
        self.exposure = exposure
        return self.get_exposure()

    def get_exposure(self) -> Q_:
        self.exposure = float(self.camera.ExposureTime.ToString()) * Q_('us')
        return self.exposure

    def read_camera(self):
        if not self.camera.IsGrabbing():
            raise WrongCameraState('You need to trigger the camera before reading from it')

        if self.mode == self.MODE_SINGLE_SHOT:
            grab = self.camera.RetrieveResult(int(self.exposure.m_as('ms')) + 100, pylon.TimeoutHandling_Return)
            img = [grab.Array]
            grab.Release()
            self.camera.StopGrabbing()
        else:
            img = []
            num_buffers = self.camera.NumReadyBuffers.Value
            logger.debug(f'{self.camera.NumQueuedBuffers.Value} frames available')
            if num_buffers:
                img = [None] * num_buffers
                for i in range(num_buffers):
                    grab = self.camera.RetrieveResult(int(self.exposure.m_as('ms')) + 100, pylon.TimeoutHandling_Return)
                    if grab:
                        img[i] = grab.Array
                        grab.Release()
        return [i.T for i in img]  # Transpose to have the correct size

    def stop_acquisition(self):
        logger.info('Stopping acquisition')
        self.camera.StopGrabbing()
        self.camera.AcquisitionStop.Execute()

    def stop_camera(self):
        logger.info('Stopping camera')
        self.stop_acquisition()
        self.camera.Close()

    def __str__(self):
        if self.friendly_name:
            return self.friendly_name
        return "Basler Camera"


if __name__ == '__main__':
    from time import sleep

    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    logger.info('Starting Basler')
    basler = Camera(0)
    basler.initialize()
    basler.set_acquisition_mode(basler.MODE_SINGLE_SHOT)
    basler.set_exposure(Q_('.02s'))
    basler.trigger_camera()
    print(len(basler.read_camera()))
    basler.set_acquisition_mode(basler.MODE_CONTINUOUS)
    basler.trigger_camera()
    sleep(1)
    imgs = basler.read_camera()
    print(len(imgs))
