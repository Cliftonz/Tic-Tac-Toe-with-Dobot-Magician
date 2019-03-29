import numpy as np
import cv2

if __name__ == '__main__':
    cam = cv2.VideoCapture(0)
    s, im = cam.read()  # captures image
    #cv2.imshow("Test Picture", im)  # displays captured image
    cv2.imwrite("test.bmp", im)  # writes image test.bmp to disk

    lineThickness = 2

    #Right box top line
    cv2.line(im, (356, 94), (620, 94), (255, 0, 0), lineThickness)

    #Right box right line
    cv2.line(im, (620, 94), (620, 352), (255, 0, 0), lineThickness)

    #Right box bottom line
    cv2.line(im, (620 , 352), (356, 349), (255, 0, 0), lineThickness)

    #Right box left line
    cv2.line(im, (356, 349), (356, 94), (255, 0, 0), lineThickness)

    #Add left box

    #Left Box Top line
    cv2.line(im, (46, 91), (300, 93), (255, 0, 0), lineThickness)

    #Left Box right line
    cv2.line(im, (300, 93), (299, 348), (255, 0, 0), lineThickness)

    #Left Box bottom line
    cv2.line(im, (299, 348), (39, 348), (255, 0, 0), lineThickness)

    #Left Box left line
    cv2.line(im, (39, 348), (46, 91), (255, 0, 0), lineThickness)

    cv2.imwrite("testOL.bmp", im)
