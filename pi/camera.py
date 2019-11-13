from tqdm import tqdm
# import io
from time import sleep
from PIL import Image
from threading import Lock
import picamera
import numpy as np
import picamera.array
from image_interpreter import get_pixel_error_from_image


class Camera:
    def __init__(self, width=640, height=480):
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
        
        self.stream = picamera.array.PiRGBArray(self.camera, size=(self.width, self.height))
        self.raw_buffer = picamera.array.PiRGBArray(self.camera, size=(self.width, self.height))
        self.lock = Lock()
        self.cur_error = 0
        self.should_stop = False


    def process_image(self, frame):
        #process image here
        error = get_pixel_error_from_image(frame)
        print(error)
        return error


    def start_capture(self):
        for iteration in self.camera.capture_continuous(self.stream, format="rgb", use_video_port=True):
            if(self.should_stop):
                return
            self.stream.truncate()
            self.stream.seek(0)
            ## get the error of the current frame
            error = self.process_image(self.stream)
            self.lock.acquire()
            self.cur_error = error
            self.lock.release()


    def get_error(self):
        self.lock.acquire()
        error = self.cur_error
        self.lock.release()
        self.camera.close()
        return error
