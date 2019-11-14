# This is the image interpreter for
# CS 503 SP19 Duckie Town project Team 4
#
# Code to check lane following via vision.


import os
import PIL.Image as Image
import numpy as np

# variables
crop_percentage = 0.05
down_sample_steps = 8

# single image process
# link to images
parent_dir = os.path.dirname(os.getcwd())
image_path = os.path.join(parent_dir, 'test_road_images/')



def get_pixel_error_from_image(frame):
    if(!init_roi):
        init_roi = True

    image_in = Image.fromarray(frame)
    # numimg = np.array(image_in)
    # convert to hue
    # hsv = image_in.convert('HSV')
    # pixel_val_hsv = np.array(hsv)
    height, width, depth = frame.shape

    # look for specific range for different colors to define roi
    a = frame[height//2-(int(height*crop_percentage)):height//2+(int(height*crop_percentage)), : , :]
    # print(a.shape)
    # # to display an image
    # b = Image.fromarray(a, 'HSV')
# =============================================================================
#     b = Image.fromarray(a[:,:], 'RGB')
#     # c = b.convert('RGB')
#     # c.save(image_path + 'strtA_crop15perc.jpg')
#     b.show()
# =============================================================================

    #convert one RGB pixel to HSV
    def RGBtoHSV(rgb):
        r = rgb[0] / 255.0
        g = rgb[1] / 255.0
        b = rgb[2] / 255.0
        mn = min(r,g,b)
        mx = max(r,g,b) 
        dc = mx - mn
        h = 0
        s = 0
        v = 0
        
        #calculate Hue (unit: degrees)
        if(dc == 0):
            h = 0
        elif(r == mx):
            h = 60 * (((g - b)/dc) % 6)
        elif(g == mx):
            h = 60 * (((b - r)/dc) + 2)
        else:
            h = 60 * (((r - g)/dc) + 4)

        #calculate Saturation (unit: pct)
        if(mx == 0):
            s = 0
        else:
            s = dc / mx

        #calculate Value (unit: pct)
        v = mx

        h = h * (255.0/360)
        s = s * (255.0)
        v = v * (255.0)

        return (int(h),int(s),int(v))

    #check if a pixel is black
    def isBlack(hsv_color):
        return 1 if v < 20 else 0

    #For yellow color a hue range from 51 degree to 60 degree has been defined
    def isYellow(hsv_color):
        h, s, v = hsv_color
        if 30 <= h <= 60:
            if 100 <= s <=255:
                return 255
            else:
                return 0
        else:
            return 0

    

    def isWhite(hsv_color):
        h, s, v = hsv_color
        if 0 <= s <= 15:
            if 240 <= v <=255:
                return 255
            else:
                return 0
        else:
            return 0

    def isRed(hsv_color):
        h,s,v = hsv_color
        if 240 <= h <= 255:
            if 125 <= s <=255:
                return 1
            else:
                return 0
        else:
            return 0


    yellowStrip = np.zeros((a.shape[0],a.shape[1]//down_sample_steps),dtype=a.dtype)
    whiteStrip = np.zeros((a.shape[0],a.shape[1]//down_sample_steps),dtype=a.dtype)
    redStrip = np.zeros((a.shape[0],a.shape[1]//down_sample_steps),dtype=a.dtype)
# =============================================================================
#     reducedImage = np.zeros((a.shape[0],a.shape[1]//4,a.shape[2]),dtype=a.dtype)
# =============================================================================
    for M in range(whiteStrip.shape[0]):
        for N in range(whiteStrip.shape[1]):

            pixel = RGBtoHSV(a[M,down_sample_steps*N])
            whiteStrip[M,N] = isWhite(pixel)
            yellowStrip[M,N] = isYellow(pixel)
            redStrip[M,N] = isRed(pixel)

# =============================================================================
#     b = Image.fromarray(redStrip, 'L')
#     c = b.convert('RGB')
#     c.show()
# =============================================================================
# =============================================================================
# 
#     calculate the distance of lane center and image center
# =============================================================================
    yelColSum = np.sum(yellowStrip, axis=0)
    yelEdge = np.argmax(yelColSum)

    whiColSum = np.sum(whiteStrip, axis=0)
    whiEdge = whiteStrip.shape[1] - np.argmax(np.flipud(whiColSum)) -1

    #print('yelEdge=',yelEdge,' WhiEdge=',whiEdge)

    laneCenter = int(np.mean([whiEdge,yelEdge]))
    imageCenter = whiteStrip.shape[1]//2
 
    #print('ImCenter=',imageCenter,'  lCenter=',laneCenter)
    error = laneCenter - imageCenter

    redRowSum = np.sum(redStrip, axis = 1)


    # TODO: implement this part
    saw_red = False

    if redRowSum[10] >= (0.4*redStrip.shape[1]):
        saw_red = True



    return (error, saw_red)

    # TODO:
    # take center of the image as reference point
    # define constants w.r.t real world:
        # every thing in pixel position/indices
        # ideal_y as the (average of distance from inner yellow and white edges - center of image)
    # for each new image
    # loop through each row
        # reference(current_r) = average of inner yellow line and inner white line
        # current_y = calculate the average, then subtract the center (c)
        # compare to ideal_y
        # convert difference in pixel to distance(cm)
        # sent to PD controller


if __name__ == "__main__":
    # read in image
    image_in = Image.open(image_path + 'dist_to_red_15cm.png', 'r')
    rgb_frame = np.array(image_in)
    error = get_pixel_error_from_image(rgb_frame)
    print(error)
