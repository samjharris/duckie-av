# This is the image interpreter for
# CS 503 SP19 Duckie Town project Team 4
#
# Code to check lane following via vision.


import os
import PIL.Image as Image
import numpy as np

# variables
crop_percentage = 0.1


# single image process
# link to images
parent_dir = os.path.dirname(os.getcwd())
image_path = os.path.join(parent_dir, 'test_road_images/')


def get_pixel_error_from_image(frame):
    image_in = Image.fromarray(frame)

    # convert to hue
    hsv = image_in.convert('HSV')
    pixel_val_hsv = np.array(hsv)
    height, width, depth = pixel_val_hsv.shape

    # look for specific range for different colors to define roi
    a = pixel_val_hsv[height//2-(int(height*crop_percentage)):height//2+(int(height*crop_percentage)), : , :]

    # # to display an image
    # b = Image.fromarray(a, 'HSV')
    # #b = Image.fromarray(a[:,200:310,0], 'L')
    # c = b.convert('RGB')
    # c.save(image_path + 'strtA_crop15perc.jpg')
    # c.show()


    #For yellow color a hue range from 51° to 60° has been defined
    def isYellow(hsv_color):
        h, s, v = hsv_color
        return 1 if 35 <= h <= 40 else 0


    yellowStrip = np.zeros((a.shape[0],a.shape[1]//4),dtype=a.dtype)
    for M in range(yellowStrip.shape[0]):
        for N in range(yellowStrip.shape[1]):
            yellowStrip[M,N] = isYellow(a[M,4*N])

    # b = Image.fromarray(yellowStrip, 'L')
    # c = b.convert('RGB')
    # c.show()

    yelColSum = np.sum(yellowStrip, axis=0)
    yelEdge = np.argmax(yelColSum)



    def isWhite(hsv_color):
        h, s, v = hsv_color
        if 0 <= s <= 15:
            if 240 <= v <=255:
                return 1
            else:
                return 0
        else:
            return 0

    whiteStrip = np.zeros((a.shape[0],a.shape[1]//4),dtype=a.dtype)
    for M in range(whiteStrip.shape[0]):
        for N in range(whiteStrip.shape[1]):
            whiteStrip[M,N] = isWhite(a[M,4*N])

    # b = Image.fromarray(whiteStrip, 'L')
    # c = b.convert('RGB')
    # c.show()

    whiColSum = np.sum(whiteStrip, axis=0)
    whiEdge = whiteStrip.shape[1] - np.argmax(np.flipud(whiColSum)) -1

    laneCenter = np.mean([whiEdge,yelEdge])
    imageCenter = whiteStrip.shape[1]//2

    error = laneCenter - imageCenter

    # TODO: implement this part
    saw_red = False

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
    image_in = Image.open(image_path + '20cmfromred_left_twocm_right_onehalfcm.jpg', 'r')
    rgb_frame = np.array(image_in)
    error = get_pixel_error_from_image(rgb_frame)
    print(error)
