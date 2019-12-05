# CICS 503 Fall 2019 DuckieTown Group 4
#
# camera.py:
# provides a class wrapping the picamera
# module for use in our robot's capturing
# and processing of images

from config import *
from tqdm import tqdm
# import io
from time import sleep
from threading import Lock, Thread
import picamera
import picamera.array
from image_processing import get_pixel_error_from_image


class Camera():
    def __init__(self, width=640, height=480):
        self.width, self.height = width, height
        self.lock = Lock()
        # self.cur_error = 0
        self.should_stop = False
        self.cur_frame = None

        # start a thread to start capturing video
        video_thread = Thread(target=self.start_capture)
        video_thread.start()

    def start_capture(self):
        with tqdm(desc="camera") as pbar:
            with picamera.PiCamera() as camera:
                # properly set up the camera
                camera.resolution = (self.width, self.height)
                # camera.framerate = 60

                # start capturing frames, continuously updating the current frame (self.cur_frame)
                with picamera.array.PiRGBArray(camera) as stream:  #TODO: this line should probably be deleted
                        rawCapture = picamera.array.PiRGBArray(camera, size=(self.width, self.height))
                        stream = camera.capture_continuous(rawCapture, format="rgb", use_video_port=True)
                        for f in stream:
                            if self.should_stop:
                                break
                            rawCapture.truncate(0)
                            self.cur_frame = f.array
                            # pbar.update()  # only to measure framerate

    def get_error(self, turn_direction):
        if self.cur_frame is None:
            return 0, True
        cur_error, saw_red, saw_green = get_pixel_error_from_image(self.cur_frame, turn_direction)
        return cur_error, saw_red, saw_green
