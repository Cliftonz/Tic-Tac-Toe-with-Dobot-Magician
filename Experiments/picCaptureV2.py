import numpy as np
import math
import cv2

if __name__ == '__main__':

    cam = cv2.VideoCapture(0)
    s, frame = cam.read()  # captures image

    cam.release()

    OuterThickness = 2
    InnerThickness = 1

    rp1 = (360, 83)
    rp2 = (635, 355)

    lp1 = (29, 82)
    lp2 = (299, 350)

    # Right square
    cv2.rectangle(frame, rp1, rp2, (0, 255, 0), OuterThickness)

    # left square
    cv2.rectangle(frame, lp1, lp2, (255, 0, 0), OuterThickness)

    RXBlockSize = math.ceil((rp2[0] - rp1[0]) / 3)

    RYBlockSize = math.ceil((rp2[1] - rp1[1]) / 3)

    LXBlockSize = math.ceil((lp2[0] - lp1[0]) / 3)

    LYBlockSize = math.ceil((lp2[1] - lp1[1]) / 3)

    # cv2.rectangle(frame, rp1, rp2, (0, 255, 0), OuterThickness)

    # Right Sub boxes
    for i in range(0, 3):
        for k in range(0, 3):
            cv2.rectangle(frame,
                          (rp1[0] + k * RXBlockSize, rp1[1] + i * RYBlockSize),
                          (rp1[0] + (k + 1) * RXBlockSize, rp1[1] + (i + 1) * RYBlockSize),
                          (50 + 20 * (i + k), 0 + 30 * (i + k), 100),
                          InnerThickness)

    # Left sub boxes
    # !!!IMPORTANT!!!
    for i in range(0, 3):
        for k in range(0, 3):
            cv2.rectangle(frame,
                          (lp1[0] + k * LXBlockSize, lp1[1] + i * LYBlockSize),
                          (lp1[0] + (k + 1) * LXBlockSize, lp1[1] + (i + 1) * LYBlockSize),
                          (10 * (i + k), 0 + 10 * (i + k), 0),
                          InnerThickness)
    while True:

        cv2.imshow('preview 1', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break



    cv2.destroyAllWindows()

    cv2.imwrite("testOLV2.bmp", frame)
