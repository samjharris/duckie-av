from tqdm import tqdm
# import io
from time import sleep
import picamera
import numpy as np
import picamera.array

# w, h = 640, 480
w, h = 320, 240

def process(frame):
    # from PIL import Image
    # img = Image.fromarray(frame, 'RGB')
    # img.save('my.png')
    # img.show()

    # print(frame.shape, w*h)
    pass


with picamera.PiCamera() as camera:
    camera.resolution = (w, h)
    # camera.framerate = 30

    # expose the camera properly
    sleep(2)
    camera.shutter_speed = camera.exposure_speed
    camera.exposure_mode = 'off'
    g = camera.awb_gains
    camera.awb_mode = 'off'
    camera.awb_gains = g


    with picamera.array.PiRGBArray(camera) as stream:
        with tqdm(total=1) as pbar:

            rawCapture = picamera.array.PiRGBArray(camera, size=(w, h))
            stream = camera.capture_continuous(rawCapture, format="rgb", use_video_port=True)

            for f in stream:
                rawCapture.truncate(0)
                process(f.array)
                pbar.update()

                break
