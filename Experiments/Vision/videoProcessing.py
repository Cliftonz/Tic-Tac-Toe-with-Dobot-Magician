
import cv2
import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

if __name__ == '__main__':
    # cv2.namedWindow("Preview")
    vc = cv2.VideoCapture(0)
    # disparity constant
    numDisparities = 16
    blockSize = 15
    # try to get the first frame
    if vc.isOpened():
        rval, frame = vc.read()
    else:
        rval = False

    while rval:
        cv2.imshow("preview", frame)
        imgL = cv.imread(frame, 0)
        imgR = cv.imread(frame, 0)
        stereo = cv.StereoBM_create(numDisparities, blockSize)
        disparity = stereo.compute(imgL, imgR)
        plt.imshow(disparity, 'gray')
        # plt.show()
        #cv2.imshow("Disparity", disparity)

        # new input
        rval, frame = vc.read()
        key = cv2.waitKey(20)
        if key == 27: # exit on ESC
            break

    cv2.destroyWindow("preview")
    vc.release()