
import cv2
import numpy as np

if __name__ == '__main__':
    img1 = cv2.imread("NoCircle.jpg")
    img2 = cv2.imread("Hand.jpg")

    diff = cv2.absdiff(img1, img2)
    
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

    # find the nozero regions in the gray
    imask =  gray>0

    # create a Mat like img2
    canvas = np.zeros_like(img2, np.uint8)

    # set mask
    canvas[imask] = img2[imask]

    cv2.imwrite("result.png", canvas)

    #cv2.imshow("result.png", canvas)
