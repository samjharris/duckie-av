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
from colorsys import rgb_to_hsv


# testing imports
#import time

# variables
crop_percentage = 0.05
down_sample_steps = 8

# single image process
# link to images
parent_dir = os.path.dirname(os.getcwd())
image_path = os.path.join(parent_dir, 'test_road_images/')
#image_path = os.path.join(parent_dir, 'test_road_images\\')


# https://stackoverflow.com/a/38059401/2230446
def rgb_to_hsv_vectorized(img): # img with BGR format
    maxc = img.max(-1)
    minc = img.min(-1)

    out = np.zeros(img.shape)
    out[:,:,2] = maxc
    out[:,:,1] = (maxc-minc) / maxc

    divs = (maxc[...,None] - img)/ ((maxc-minc+1)[...,None])
    cond1 = divs[...,0] - divs[...,1]
    cond2 = 2.0 + divs[...,2] - divs[...,0]
    h = 4.0 + divs[...,1] - divs[...,2]
    h[img[...,2]==maxc] = cond1[img[...,2]==maxc]
    h[img[...,1]==maxc] = cond2[img[...,1]==maxc]
    out[:,:,0] = (h/6.0) % 1.0

    out[minc == maxc,:2] = 0
    return out

def RGBtoHSV(rgb):
    h, s, v = rgb_to_hsv(*(rgb/255))
    h, s, v = int(255*h), int(255*s), int(255*v)
    return h, s, v


# #check if a pixel is black
# def isBlack(hsv_color):
#     h, s, v = hsv_color
#     # from testing various sample images, black 
#     # seems to be v<40%, so 40% * 255 =  102 
#     if v < 102:
#         return 1
#     return 0

# #For yellow color a hue range from 51 degree to 60 degree has been defined
# def isYellow(hsv_color):
#     h, s, v = hsv_color
#     if 30 <= h <= 60:
#         if 100 <= s <=255:
#             return 255
#         else:
#             return 0
#     else:
#         return 0

# def isWhite(hsv_color):
#     h, s, v = hsv_color
#     if 0 <= s <= 15:
#         if 240 <= v <=255:
#             return 255
#         else:
#             return 0
#     else:
#         return 0

# def isRed(hsv_color):
#     h,s,v = hsv_color
#     if 240 <= h <= 255:
#         if 125 <= s <=255:
#             return 1
#         else:
#             return 0
#     else:
#         return 0


def isBlackVectorized(hsv_image):
    return hsv_image[:,:,2] <= 102

def isYellowVectorized(hsv_image):
    return (hsv_image[:,:,1] >= 100) & (30 <= hsv_image[:,:,0]) & (hsv_image[:,:,0] <= 120)

def isWhiteVectorized(hsv_image):
    return (hsv_image[:,:,1] <= 50) & (hsv_image[:,:,2] >= 220)

def isRedVectorized(hsv_image):
    return (hsv_image[:,:,1] >= 125) & (hsv_image[:,:,0] >= 240)


def get_pixel_error_from_image(frame):
    #t = time.time_ns()
    height, width, depth = frame.shape

    # crop a horizontal strip from the center
    a = frame[height//2-int(height*crop_percentage):height//2+int(height*crop_percentage), ::down_sample_steps , :]


    # yellowStrip = np.zeros((a.shape[0],a.shape[1]//down_sample_steps),dtype=a.dtype)
    # whiteStrip = np.zeros((a.shape[0],a.shape[1]//down_sample_steps),dtype=a.dtype)
    # redStrip = np.zeros((a.shape[0],a.shape[1]//down_sample_steps),dtype=a.dtype)


    # cntYellow = 0
    # cntWhite = 0
    # for M in range(whiteStrip.shape[0]):
    #     for N in range(whiteStrip.shape[1]):

    #         pixel = RGBtoHSV(a[M,down_sample_steps*N])
    #         #ignore black pixels 
    #         if(isBlack(pixel)):
    #             continue
    #         #if(isWhite(pixel)):
    #         if(cntWhite < 3 and isWhite(pixel)):
    #             whiteStrip[M,N] = 255
    #             cntWhite += 1
    #             continue
    #         # if(isYellow(pixel)):
    #         if(cntYellow < 3 and isYellow(pixel)):
    #             yellowStrip[M,N] = 255
    #             cntYellow += 1
    #             continue
    #         if(isRed(pixel)):
    #             redStrip[M,N] = 1
    #             continue

    # hsvStrip = RGBtoHSV(a[:,::down_sample_steps])
    # hsv_output = rgb_to_hsv_vectorized(a)
    # hsv_output = np.array(Image.fromarray(a).convert('HSV'))
    hsvStrip = np.array(Image.fromarray(a).convert('HSV'))
    # print(hsv_output[:,:,0].min(), hsv_output[:,:,0].max())
    # print(hsv_output[:,:,1].min(), hsv_output[:,:,1].max())
    # print(hsv_output[:,:,2].min(), hsv_output[:,:,2].max())
    # print(hsv_output[8:20,8:20,0])

    # hsvStrip = (hsv_output*255).astype(np.uint8)
    # hsvStrip[:,:,0] = 255-hsvStrip[:,:,0]
    # hsvStrip[:,:,2] = 255-hsvStrip[:,:,2]


    # blackStrip = np.zeros((hsvStrip.shape[0],hsvStrip.shape[1]), dtype=hsvStrip.dtype)
    yellowStrip = np.zeros((hsvStrip.shape[0],hsvStrip.shape[1]), dtype=hsvStrip.dtype)
    whiteStrip = np.zeros((hsvStrip.shape[0],hsvStrip.shape[1]), dtype=hsvStrip.dtype)
    redStrip = np.zeros((hsvStrip.shape[0],hsvStrip.shape[1]), dtype=hsvStrip.dtype)


    # # to display an image
    # b = Image.fromarray(hsvStrip[:,:,0], 'L')
    # c = b.convert('RGB')
    # c.save(image_path + 'test.jpg')
    # print("done")

    # print(hsvStrip[:4,:4,:])
    # blackStrip[isBlackVectorized(hsvStrip)] = 255
    whiteStrip[isWhiteVectorized(hsvStrip)] = 255
    yellowStrip[isYellowVectorized(hsvStrip)] = 255
    redStrip[isRedVectorized(hsvStrip)] = 255

    # # display image
    # Image.fromarray(a, 'RGB').convert('RGB').save(image_path + 'test_rgb.jpg')
    # Image.fromarray(hsvStrip, 'HSV').convert('RGB').save(image_path + 'test_hsv.jpg')
    # Image.fromarray(whiteStrip, 'L').convert('RGB').save(image_path + 'test_white.jpg')
    # Image.fromarray(yellowStrip, 'L').convert('RGB').save(image_path + 'test_yellow.jpg')
    # Image.fromarray(redStrip, 'L').convert('RGB').save(image_path + 'test_red.jpg')
    # print("done")



# =============================================================================
# 
#     calculate the distance of lane center and image center
# =============================================================================

    # print(yellowStrip.shape)
    yelColSum = np.sum(yellowStrip, axis=0)
    yelEdge = np.argmax(yelColSum)

    whiColSum = np.sum(whiteStrip, axis=0)
    whiEdge = whiteStrip.shape[1] - np.argmax(np.flipud(whiColSum)) -1

    # print(yelColSum)
    # print(whiColSum)
    # print("="*15)


    laneCenter = 0
    imageCenter = 0
    # if both edges are visible
    # TODO: NOT FULLY TESTED YET!!!!
    if yelEdge > 0 and whiEdge < 79:
        if yelEdge < whiEdge:
            # calculate lane center using both edge and image center using the white
            laneCenter = int(np.mean([whiEdge,yelEdge]))
            imageCenter = whiteStrip.shape[1]//2
        else:
            laneCenter = int(yelEdge + LANE_WIDTH_PIX / 2)
            imageCenter = yellowStrip.shape[1]//2
        
     
    # else if only one edge is visible
    else:
        # if only white is visible, calculate everything using white
        if whiEdge < 79 and yelEdge == 0:
            laneCenter = int(whiEdge - LANE_WIDTH_PIX / 2)
            imageCenter = whiteStrip.shape[1]//2
        # else if only yellow is visible, calculate everything using yellow
        elif whiEdge == 79 and yelEdge > 0:
            laneCenter = int(yelEdge + LANE_WIDTH_PIX / 2)
            imageCenter = yellowStrip.shape[1]//2
        # else both are invisible, stop?
    
    error = laneCenter - imageCenter
    # check if see red in front 
    saw_red = False
    
    redRowSum = np.sum(redStrip, axis = 1)

    if redRowSum[10] >= (0.4*redStrip.shape[1]):
        saw_red = True

    #dt = time.time_ns()
    if DEBUG_INFO_ON:
        print("Image Interpreter")
        print("{:>22} : {}".format("yelEdge", yelEdge))
        print("{:>22} : {}".format("whiEdge", whiEdge))
        print("{:>22} : {}".format("imageCenter", imageCenter))
        print("{:>22} : {}".format("laneCenter", laneCenter))
        print("{:>22} : {}".format("error", error))
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
        error = get_pixel_error_from_image(rgb_frame)
        print(error)


