from tqdm import tqdm
# import io
from time import sleep
from PIL import Image
from threading import Lock, Thread
import picamera
import numpy as np
import picamera.array
from image_interpreter import get_pixel_error_from_image


class Camera():
    def __init__(self, width=640, height=480):
        self.width, self.height = width, height
        self.lock = Lock()
        self.cur_error = 0
        self.should_stop = False

        # start a thread to start capturing video
        video_thread = Thread(target=self.start_capture)
        video_thread.start()


    def start_capture(self):
        with picamera.PiCamera() as camera:
            camera.resolution = (self.width, self.height)
            # camera.framerate = 30

            # expose the camera properly
            sleep(2)
            camera.shutter_speed = camera.exposure_speed
            camera.exposure_mode = 'off'
            g = camera.awb_gains
            camera.awb_mode = 'off'
            camera.awb_gains = g

            with picamera.array.PiRGBArray(camera) as stream:
                    rawCapture = picamera.array.PiRGBArray(camera, size=(self.width, self.height))
                    stream = camera.capture_continuous(rawCapture, format="rgb", use_video_port=True)

                    for f in stream:
                        if self.should_stop:
                            break

                        rawCapture.truncate(0)

                        self.process(f.array)


    def process(self, frame):
        # from PIL import Image
        # img = Image.fromarray(frame, 'RGB')
        # img.save('my.png')
        # img.show()

        # print(frame.shape, self.width*self.height)

        #process image here
        error, saw_red = get_pixel_error_from_image(frame)
        print("error: {}  saw red: {}".format(error, saw_red))

        # set the error
        self.lock.acquire()
        self.cur_error = error
        self.should_stop = saw_red
        self.lock.release()


    def get_error(self):
        self.lock.acquire()
        error = self.cur_error
        saw_red = self.should_stop
        self.lock.release()
        return error, saw_red
