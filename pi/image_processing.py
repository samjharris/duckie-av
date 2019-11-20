# CICS 503 Fall 2019 DuckieTown Group 4
#
# image_processing.py:
# provides functions for computing
# pixel error-margins from images
# captured by our robot

from config import *
import os
import PIL.Image as Image
import numpy as np


# variables
crop_percentage = 0.05
down_sample_steps = 8
min_percentage_red_threshold = 0.5  # TODO: tune this value

parent_dir = os.path.dirname(os.getcwd())
image_path = os.path.join(parent_dir, 'test_road_images/')
#image_path = os.path.join(parent_dir, 'test_road_images\\')


def is_yellow_vectorized(hsv_image):
    return (hsv_image[:,:,1] >= 150) & (30 <= hsv_image[:,:,0]) & (hsv_image[:,:,0] <= 50)

def is_white_vectorized(hsv_image):
    return (hsv_image[:,:,1] <= 50) & (hsv_image[:,:,2] >= 220)

def is_red_vectorized(hsv_image):
    return (hsv_image[:,:,1] >= 125) & (hsv_image[:,:,0] >= 240)


def get_pixel_error_from_image(frame):
    height, width, depth = frame.shape

    # crop a horizontal strip from the center
    rgb_strip = frame[height//2-int(height*crop_percentage):height//2+int(height*crop_percentage), ::down_sample_steps , :]

    # convert the strip to hsv
    hsv_strip = np.array(Image.fromarray(rgb_strip).convert('HSV'))


    yellow_strip = np.zeros((hsv_strip.shape[0],hsv_strip.shape[1]), dtype=hsv_strip.dtype)
    white_strip = np.zeros((hsv_strip.shape[0],hsv_strip.shape[1]), dtype=hsv_strip.dtype)
    red_strip = np.zeros((hsv_strip.shape[0],hsv_strip.shape[1]), dtype=hsv_strip.dtype)


    white_strip[is_white_vectorized(hsv_strip)] = 255
    yellow_strip[is_yellow_vectorized(hsv_strip)] = 255
    red_strip[is_red_vectorized(hsv_strip)] = 255

    # # write images to files for debugging (turn off when not debugging)
    # Image.fromarray(a, 'RGB').convert('RGB').save(image_path + 'test_rgb.jpg')
    # Image.fromarray(hsv_strip, 'HSV').convert('RGB').save(image_path + 'test_hsv.jpg')
    # Image.fromarray(white_strip, 'L').convert('RGB').save(image_path + 'test_white.jpg')
    # Image.fromarray(yellow_strip, 'L').convert('RGB').save(image_path + 'test_yellow.jpg')
    # Image.fromarray(red_strip, 'L').convert('RGB').save(image_path + 'test_red.jpg')
    # print("done")



# =============================================================================
#
#     calculate the distance of lane center and image center
# =============================================================================


    yel_col_sum = np.sum(yellow_strip, axis=0) > 0
    yel_edge = np.argmax(yel_col_sum)

    whi_col_sum = np.sum(white_strip, axis=0) > 0
    whi_edge = len(whi_col_sum) - np.argmax(np.flipud(whi_col_sum)) -1


    percentage_red = np.sum(red_strip) / np.prod(red_strip.shape)
    saw_red = percentage_red > min_percentage_red_threshold
    # print("percentage_red", percentage_red)

    saw_white = (whi_edge != len(whi_col_sum)-1)
    saw_yellow = (yel_edge != 0)

    image_center = white_strip.shape[1] // 2

    if saw_white and saw_yellow:
        lane_center = np.mean([yel_edge, whi_edge])
    elif saw_white and not saw_yellow:
        lane_center = whi_edge - LANE_WIDTH_PIX // 2
    elif not saw_white and saw_yellow:
        lane_center = yel_edge + LANE_WIDTH_PIX // 2
    else:
        # we saw neither white nor yellow
        lane_center = image_center

    error = lane_center - image_center

    if DEBUG_INFO_ON:
        print("Image Processing")
        print("{:>22} : {}".format("yel_edge", yel_edge))
        print("{:>22} : {}".format("whi_edge", whi_edge))
        print("{:>22} : {}".format("image_center", image_center))
        print("{:>22} : {}".format("lane_center", lane_center))
        print("{:>22} : {}".format("error", error))
        print("{:>22} : {}".format("saw_red", saw_red))
        print("="*30)

    return (error, saw_red)


if __name__ == "__main__":

    # # read in image
    # image_in = Image.open(image_path + 'dist_to_red_15cm.png', 'r')
    # rgb_frame = np.array(image_in)
    # error = get_pixel_error_from_image(rgb_frame)
    # print(error)


    import picamera, time
    with picamera.PiCamera() as camera:
        w, h = 640, 480
        camera.resolution = (w, h)
        camera.framerate = 24
        time.sleep(2)
        rgb_frame = np.empty((h, w, 3), dtype=np.uint8)
        camera.capture(rgb_frame, 'rgb')
        error, saw_red = get_pixel_error_from_image(rgb_frame)
        print(error, "px error")
        print(error / PIX_PER_CM, "cm error")
