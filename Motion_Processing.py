
import datetime
import imutils
from PIL import Image
import cv2


def has_changed_t2f(previous, current):
    if previous is True and current is False:
        return True
    else:
        return False


def wait_for_player_move(capture, show_windows):

    # initialize the first frame in the video stream
    first_frame = None

    # 500 is a good minimum for finding contours
    min_area = 700

    # If motion has been detect wait 5 second after motion ends
    # then break out of loop
    previous_movement = False
    current_movement = False

    end_time = datetime.datetime.now() + datetime.timedelta(0, 30)

    emergency_end_time = datetime.datetime.now() + datetime.timedelta(0, 30)

    # loop over the frames of the video
    while True:
        # grab the current frame and initialize the occupied/unoccupied text
        if not (capture.grab()):
            print("No more frames")
            break

        current_time = datetime.datetime.now()

        # if movement was detected and then not detected
        # wait 5 seconds to see if there is any more movement
        # if has_changed_t2f(previous_movement, current_movement) and player_move_ended is False:
        if has_changed_t2f(previous_movement, current_movement):
            end_time = current_time + datetime.timedelta(0, 3)

        previous_movement = current_movement

        # Capture frame-by-frame
        ret, frame = capture.read()

        text = "No Movement Detected"

        # resize the frame, convert it to grayscale, and blur it
        width = 500
        frame = imutils.resize(frame, width)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        # if the first frame is None, initialize it
        if first_frame is None:
            first_frame = gray
            continue

        # compute the absolute difference between the current frame and first frame
        frame_delta = cv2.absdiff(first_frame, gray)
        thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]

        # dilate the thresholded image to fill in holes, then find contours on thresholded image
        iterations = 2
        thresh = cv2.dilate(thresh, None, iterations)
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        current_movement = False
        # loop over the contours
        for c in cnts:

            # if the contour is too small, ignore it
            if cv2.contourArea(c) < min_area:
                continue

            current_movement = True

            # compute the bounding box for the contour, draw it on the frame,
            # and update the text
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            text = "MOVEMENT DETECTED"

        if show_windows is True:
            # draw the text and timestamp on the frame
            cv2.putText(frame, "Board Status: {}".format(text), (10, 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

            time_left = end_time - current_time

            cv2.putText(frame, "Time Left: {}".format(time_left), (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

            # show the frame and record if the user presses a key
            cv2.imshow('video', frame)

            cv2.imshow("Thresh", thresh)

            cv2.imshow("Frame Delta", frame_delta)

            key = cv2.waitKey(1)

            # if the `q` key is pressed, break from the lop
            if key == ord("q") or key == 13:
                break

        if current_time.time() >= end_time.time() or current_time.time() >= emergency_end_time.time():
            cv2.destroyAllWindows()
            break
