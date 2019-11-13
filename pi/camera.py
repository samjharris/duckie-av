from tqdm import tqdm
# import io
from time import sleep
from PIL import Image
from threading import Lock, Thread
import picamera
import numpy as np
import picamera.array
from image_interpreter import get_pixel_error_from_image


class Camera:
    def __init__(self, width=640, height=480):
        self.width, self.height = width, height
        self.camera = picamera.PiCamera()
        self.camera.resolution = (width, height)
        # self.camera.framerate = 80

        ## wait for exposure/gain to adjust
        sleep(2)
        ## set exposure/gain for consistent images
        self.camera.shutter_speed = self.camera.exposure_speed
        self.camera.exposure_mode = "off"
        g = self.camera.awb_gains
        self.camera.awb_mode = "off"
        self.camera.awb_gains = g

        self.raw_capture = picamera.array.PiRGBArray(self.camera, size=(self.width, self.height))
        self.lock = Lock()
        self.cur_error = 0
        self.should_stop = False


    def process_frame(self, frame):
        #process image here
        error = get_pixel_error_from_image(frame)
        print(error)
        return error


    def start_capture_async(self):
        video_thread = Thread(target=self.start_capture)
        video_thread.start()


    def start_capture(self):
        stream = self.camera.capture_continuous(self.raw_capture, format="rgb", use_video_port=True)
        for f in stream:
            if(self.should_stop):
                return
            self.raw_capture.truncate(0)

            # process the frame
            error = self.process_frame(f.array)

            # update the pixel error (instance attribute)
            self.lock.acquire()
            self.cur_error = error
            self.lock.release()


    def get_error(self):
        self.lock.acquire()
        error = self.cur_error
        self.lock.release()
        self.camera.close()
        return error
