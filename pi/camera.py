from tqdm import tqdm
# import io
from time import sleep
from PIL import Image
from threading import Lock
import picamera
import numpy as np
import picamera.array

class camera:
    def __init__(self, width=640, height=480):
        ## initialize picamera object
        self.cam = picamera.PiCamera()
        camera.resolution = (width, height)
        #camera.framerate = 80
        ## wait for exposure/gain to adjust
        sleep(2)
        ## set exposure/gain for consistent images
        self.cam.shutter_speed = self.cam.exposure_speed
        self.cam.exposure_mode = "off"
        g = self.cam.awb_gains
        self.cam.awb_mode = "off"
        self.cam.awb_gains = g
        ## initialize the stream buffer
        self.stream = picamera.array.PiRGBArray(self.cam, size=(self.width, self.height))
        ## initialize the raw buffer
        self.raw = picamera.array.PiRGBArray(self.cam, size=(self.width, self.height))
        ## initialize the lock 
        self.lock = threading.Lock()
        ## initialize the current error to 0
        self.cur_error = 0
        ## initialize the stop signal
        self.stop = False
        return
    
    def start_capture():
        for iteration in camera.capture_continuous(self.stream, format="rgb", use_video_port=True)
            if(stop):
                return
            self.stream.truncate()
            self.stream.seek(0)
            ## get the error of the current frame
            error = process_image(self.stream)
            self.lock.acquire()
            self.cur_error = error
            self.lock.release()
    
    def process_image(frame):
        #process image here
        img = Image.fromarray(frame, 'RGB')

        return 0

    def get_error():
        self.lock.acquire()
        error = self.cur_error
        self.lock.release()
        return error



