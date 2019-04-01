from __future__ import division
# import image
from PIL import Image
import math
import numpy as np
import cv2 as cv
import os
from scipy import misc
import image_slicer


def long_slice(image_path, out_name, outdir, slice_size):
    """slice an image into parts slice_size tall"""
    img = Image.open(image_path)
    width, height = img.size
    upper = 0
    left = 0
    slices = int(math.ceil(height/slice_size))

    count = 1
    for slice in range(slices):
        #if we are at the end, set the lower bound to be the bottom of the image
        if count == slices:
            lower = height
        else:
            lower = int(count * slice_size)

        bbox = (left, upper, width, lower)
        working_slice = img.crop(bbox)
        upper += slice_size
        #save the slice
        working_slice.save(os.path.join(outdir, "slice_" + out_name + "_" + str(count)+".png"))
        count +=1


if __name__ == '__main__':
    #long_slice("CheckerBoardTest.jpg","", os.getcwd(), 300)

    img = Image.open("CheckerBoardTest.jpg")
    width = img.width
    height = img.height
    print(str(width) + "  " + str(height))
    area = (660, 50, width-100, height-50)
    cropped_img = img.crop(area)
    cropped_img.show()

   # Read the image
    # img = misc.imread("CheckerBoardTest.jpg")
    # height, width = img.shape
    #
    #Cut the image in half
    # width_cutoff = width // 2
    # s1 = img[:, :width_cutoff]
    # s2 = img[:, width_cutoff:]
    #
    #Save each half
    # misc.imsave("face1.png", s1)
    # misc.imsave("face2.png", s2)

