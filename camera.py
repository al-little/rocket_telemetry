'''Camera device'''
from device_status import DeviceStatus
from picamera import PiCamera
from enum import Enum
import datetime

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
        print('Camera: Init')

    def take_picture(self, image_path):
        self.status = CameraCommand.STILL_PHOTO
        path = image_path + image_path + 'image_' + str(datetime.datetime.utcnow()) +'.jpg'
        # Take a picture. A path is required, excluding filename.
        self.camera.capture(path)
        print('Camera: take picture ' + path)

    def start_video(self, video_path):
        if self.status != CameraCommand.START_VIDEO:
            self.status = CameraCommand.START_VIDEO
            path = video_path + video_path + 'video_' + str(datetime.datetime.utcnow()) + '.h264'
            # Start a video recording. A path is required, excluding filename.
            self.camera.start_recording(video_path + 'video_{timestamp:%H-%M-%S-%f}.h264')
            print('Camera: Start recording ' + path)

    def stop_video(self):
        self.status = CameraCommand.STOP_VIDEO
        # Stop the current recording
        self.camera.stop_recording()
        print('Camera: Stop recording')