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
min_percentage_green_threshold = 0.000 #TODO: tune this value

DEBUG_IMAGE_PROCESSING = False

parent_dir = os.path.dirname(os.getcwd())
image_path = os.path.join(parent_dir, 'test_road_images/')
#image_path = os.path.join(parent_dir, 'test_road_images\\')


def is_yellow_vectorized(hsv_image):
    return (hsv_image[:,:,1] >= 50) & (30 <= hsv_image[:,:,0]) & (hsv_image[:,:,0] <= 50)

def is_white_vectorized(hsv_image):
    return (hsv_image[:,:,1] <= 50) & (hsv_image[:,:,2] >= 220)

def is_red_vectorized(hsv_image):
    return (hsv_image[:,:,1] >= 125) & (hsv_image[:,:,0] >= 240)

def is_green_vectorized(hsv_image):
    return (hsv_image[:,:,1] >= 50) & (hsv_image[:,:,2] >= 100) & (60 <= hsv_image[:,:,0]) & (hsv_image[:,:,0] <= 170)


def super_get_pixel_error_from_image(frame, hug):
    height, width, depth = frame.shape

    # crop a horizontal strip from the center
    rgb_strip = frame[height//2 + STRIP_LOCATION*int(height*crop_percentage):height//2+(STRIP_LOCATION + 2) * int(height*crop_percentage), ::down_sample_steps , :]
    # rgb_strip = frame[height//2 + STRIP_LOCATION*int(height*crop_percentage):height//2+(STRIP_LOCATION + 2) * int(height*crop_percentage), ::down_sample_steps , :]
    DOWNSAMPLE_NUM = 2
    # gLED_strip = frame[height//2::5, width//4:width-width//4:DOWNSAMPLE_NUM, :]
    # gLED_strip = frame[height//2::5, width//4:width-width//4:DOWNSAMPLE_NUM, :]
    gLED_strip = frame[height//2::1, width//4:width-width//4:1, :]

    # convert the strip to hsv
    hsv_strip = np.array(Image.fromarray(rgb_strip).convert('HSV'))
    gLED_strip_hsv = np.array(Image.fromarray(gLED_strip).convert('HSV'))

    white_mask = is_white_vectorized(hsv_strip)
    yellow_mask = is_yellow_vectorized(hsv_strip)
    red_mask = is_red_vectorized(hsv_strip)
    green_mask = is_green_vectorized(gLED_strip_hsv)


    if DEBUG_IMAGE_PROCESSING:
        yellow_strip = np.zeros((hsv_strip.shape[0],hsv_strip.shape[1]), dtype=hsv_strip.dtype)
        white_strip = np.zeros((hsv_strip.shape[0],hsv_strip.shape[1]), dtype=hsv_strip.dtype)
        red_strip = np.zeros((hsv_strip.shape[0],hsv_strip.shape[1]), dtype=hsv_strip.dtype)
        green_strip = np.zeros((gLED_strip_hsv.shape[0],gLED_strip_hsv.shape[1]), dtype=hsv_strip.dtype)

        # write images to files for debugging (turn off when not debugging)
        white_strip[white_mask] = 255
        yellow_strip[yellow_mask] = 255
        red_strip[red_mask] = 255
        green_strip[green_mask] = 255

        Image.fromarray(frame, 'RGB').convert('RGB').save(image_path + 'frame.jpg')
        Image.fromarray(rgb_strip, 'RGB').convert('RGB').save(image_path + 'rgb_strip.jpg')
        Image.fromarray(hsv_strip[:,:,0], 'L').convert('RGB').save(image_path + 'hsv_strip.jpg')
        Image.fromarray(white_strip, 'L').convert('RGB').save(image_path + 'white_strip.jpg')
        Image.fromarray(yellow_strip, 'L').convert('RGB').save(image_path + 'yellow_strip.jpg')
        Image.fromarray(red_strip, 'L').convert('RGB').save(image_path + 'red_strip.jpg')
        Image.fromarray(green_strip, 'L').convert('RGB').save(image_path + 'green_strip.jpg')
        Image.fromarray(gLED_strip, 'RGB').convert('RGB').save(image_path + 'gLED_strip.jpg')
        print("saved images to files")



# =============================================================================
#
#     calculate the distance of lane center and image center
# =============================================================================


    yel_col_sum = np.sum(yellow_mask, axis=0)
    yel_edge = len(yel_col_sum) - np.argmax(np.flipud(yel_col_sum)) - 1

    whi_col_sum = np.sum(white_mask, axis=0)
    whi_edge = np.argmax(whi_col_sum)

    percentage_white = np.sum(white_mask) / np.prod(white_mask.shape)
    percentage_yellow = np.sum(yellow_mask) / np.prod(yellow_mask.shape)
    percentage_red = np.sum(red_mask) / np.prod(red_mask.shape)
    percentage_green = np.sum(green_mask)/np.prod(green_mask.shape)
    
    saw_red = percentage_red > min_percentage_red_threshold
    saw_white = (whi_edge != 0) and percentage_white > 0.01
    saw_yellow = (yel_edge != len(yel_col_sum)-1) and percentage_yellow > 0.01
    # print("saw_white: {}".format(saw_white))
    # print("saw_yellow: {}".format(saw_yellow))

    if saw_red:
        # print(percentage_green)
        # saw_green = np.sum(green_mask) > 5
        saw_green = percentage_green > min_percentage_green_threshold

        if saw_green:
            green_strip = np.zeros((gLED_strip_hsv.shape[0],gLED_strip_hsv.shape[1]), dtype=hsv_strip.dtype)
            green_strip[green_mask] = 255
            Image.fromarray(green_strip, 'L').convert('RGB').save(image_path + 'test_green.jpg')
            Image.fromarray(gLED_strip, 'RGB').convert('RGB').save(image_path + 'test_green2.jpg')
            print("saved green images to files")

        if DEBUG_INFO_ON:
            print("green: " + str(saw_green) + "; red: " + str(saw_red))
    else:
        saw_green = False
        
    image_center = white_mask.shape[1] // 2

    # if hug == HUG_WHITE:
    #     if saw_white:
    #         lane_center = whi_edge - WHITE_OFFSET_PIX
    #     elif not saw_white and saw_yellow:
    #         lane_center = yel_edge + LANE_WIDTH_PIX - WHITE_OFFSET_PIX
    #     else:
    #         lane_center = image_center
    # else:
    #     if saw_yellow:
    #         lane_center = yel_edge + YELLOW_OFFSET_PIX
    #     elif not saw_yellow and saw_white:
    #         lane_center = whi_edge - LANE_WIDTH_PIX + YELLOW_OFFSET_PIX
    #     else:
    #         lane_center = image_center

    if hug == HUG_WHITE:
        if saw_white:
            lane_center = whi_edge - WHITE_OFFSET_PIX
        elif not saw_white and saw_yellow:
            lane_center = yel_edge + LANE_WIDTH_PIX - WHITE_OFFSET_PIX
        else:
            lane_center = image_center
    else:
        if saw_yellow:
            lane_center = yel_edge + YELLOW_OFFSET_PIX
        elif not saw_yellow and saw_white:
            lane_center = whi_edge - LANE_WIDTH_PIX + YELLOW_OFFSET_PIX
        else:
            lane_center = image_center

    error = lane_center - image_center

    return (error, saw_red, saw_green, yel_edge/rgb_strip.shape[1])


def get_pixel_error_from_image(frame, hug):
    a, b, c, _ = super_get_pixel_error_from_image(frame, hug)
    return a,b,c


if __name__ == "__main__":
    DEBUG_IMAGE_PROCESSING = True

    import picamera, time
    with picamera.PiCamera() as camera:
        w, h = 640, 480
        camera.resolution = (w, h)
        camera.framerate = 24
        time.sleep(2)
        rgb_frame = np.empty((h, w, 3), dtype=np.uint8)
        camera.capture(rgb_frame, 'rgb')
        error, saw_red, saw_green = get_pixel_error_from_image(rgb_frame, TURN_DIRECTION)
        print(error, "px error")
        x = 2.6153846153846154
        print("PIX_PER_CM", PIX_PER_CM)

        print(error / PIX_PER_CM, "cm error")
