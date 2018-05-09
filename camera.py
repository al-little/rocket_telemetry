'''Camera device'''
from device_status import DeviceStatus
from picamera import PiCamera
from enum import Enum


class CameraCommand(Enum):
    STILL_PHOTO = 0
    START_VIDEO = 1
    STOP_VIDEO = 2


class Camera(object):
    camera = None
    status = DeviceStatus.UNINITIALISED

    def __init__(self, sensor_name):
        '''Initialise the camera with a name'''
        self.status = DeviceStatus.UNAVAILABLE
        self.sensor_name = sensor_name
        self.camera = PiCamera()
        self.status = DeviceStatus.READY

    def take_picture(self, image_path):
        '''Take a picture. A path is required, excluding filename.'''
        self.camera.capture(image_path + 'image_{timestamp:%H-%M-%S-%f}.jpg')

    def start_video(self, video_path):
        '''Start a video recording. A path is required, excluding filename.'''
        self.camera.start_recording(video_path + 'video_{timestamp:%H-%M-%S-%f}.h264')

    def stop_video(self):
        '''Stop the current recording'''
        self.camera.stop_recording()