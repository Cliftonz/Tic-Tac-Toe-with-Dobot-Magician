import numpy
import cv2
import math

if __name__ == '__main__':

    InnerThickness = 1

    rp1 = (360, 83)
    rp2 = (635, 355)

    lp1 = (29, 82)
    lp2 = (299, 350)

    cap = cv2.VideoCapture(0)

    LXBlockSize = math.ceil((lp2[0] - lp1[0]) / 3)

    LYBlockSize = math.ceil((lp2[1] - lp1[1]) / 3)

    while cv2.waitKey(1) != 27 or cv2.waitKey(1) != 113:
        if not (cap.grab()):
            print("No more frames")
            break
        # Capture frame-by-frame
        ret, frame = cap.read()

        lineThickness = 2

        # right square
        cv2.rectangle(frame, rp1, rp2, (0, 255, 0), lineThickness)

        # left square
        cv2.rectangle(frame, lp1, lp2, (255, 0, 0), lineThickness)

        for i in range(0, 3):
            for k in range(0, 3):
                cv2.rectangle(frame,
                              (lp1[0] + k * LXBlockSize, lp1[1] + i * LYBlockSize),
                              (lp1[0] + (k + 1) * LXBlockSize, lp1[1] + (i + 1) * LYBlockSize),
                              (10 * (i + k), 0 + 10 * (i + k), 0),
                              InnerThickness)

        font = cv2.FONT_HERSHEY_SIMPLEX
        bottomLeftCornerOfText = (10, 50)
        fontScale = 1
        fontColor = (255, 255, 255)
        lineType = 2

        cv2.putText(frame, 'Press \'q\' to finish set up.',
                    bottomLeftCornerOfText,
                    font,
                    fontScale,
                    fontColor,
                    lineType)

        # Display the resulting frame
        cv2.imshow('video', frame)

        c = cv2.waitKey(1)

        if c == 27 or c == 113:
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

