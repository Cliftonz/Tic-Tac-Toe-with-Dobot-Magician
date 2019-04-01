
import datetime
import imutils
import time
import cv2


if __name__ == '__main__':

    cap = cv2.VideoCapture(0)
    # initialize the first frame in the video stream
    firstFrame = None

    # 500 is a good minimum for finding contours
    min_area = 500

    count = 0

    loop = True
    # loop over the frames of the video
    while loop:
        # grab the current frame and initialize the occupied/unoccupied text
        if not (cap.grab()):
            print("No more frames")
            break

        # Capture frame-by-frame
        ret, frame = cap.read()

        text = "No Movement Detected"

        # resize the frame, convert it to grayscale, and blur it
        width = 500
        frame = imutils.resize(frame, width)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        # if the first frame is None, initialize it
        if firstFrame is None:
            firstFrame = gray
            count = 0
            continue

        # compute the absolute difference between the current frame and first frame
        frameDelta = cv2.absdiff(firstFrame, gray)
        thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

        # dilate the thresholded image to fill in holes, then find contours on thresholded image
        iterations = 2
        thresh = cv2.dilate(thresh, None, iterations)
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        # loop over the contours
        for c in cnts:
            # if the contour is too small, ignore it
            if cv2.contourArea(c) < min_area:
                continue

            # compute the bounding box for the contour, draw it on the frame,
            # and update the text
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            text = "MOVEMENT DETECTED"

        # draw the text and timestamp on the frame
        cv2.putText(frame, "Board Status: {}".format(text), (10, 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        # show the frame and record if the user presses a key
        cv2.imshow('video', frame)

        cv2.imshow("Thresh", thresh)

        cv2.imshow("Frame Delta", frameDelta)

        count += 1

        key = cv2.waitKey(1)

        # if the `q` key is pressed, break from the lop
        if key == ord("q") or key == 13:
            loop = False

    # cleanup the camera and close any open windows
    cap.release()
    cv2.destroyAllWindows()
