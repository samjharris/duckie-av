# Code from: https://picamera.readthedocs.io/en/release-1.12/recipes1.html
from picamera import PiCamera
from time import sleep

camera = PiCamera()
camera.resolution = (1024, 768)
camera.start_preview()
sleep(5)
camera.capture('image.jpg')

