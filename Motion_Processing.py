import datetime
import imutils
import cv2

previous = False


def has_changed_t2f(current):
    if globals()['previous'] is True and current is False:
        return True
    globals()['previous'] = current


def wait_for_player_move(capture):

    # initialize the first frame in the video stream
    first_frame = None

    # 500 is a good minimum for finding contours
    min_area = 500

    # If motion has been detect wait 5 second after motion ends
    # then break out of loop
    movement = False

    end_time = None
    # loop over the frames of the video
    while True:
        # grab the current frame and initialize the occupied/unoccupied text
        if not (capture.grab()):
            print("No more frames")
            break

        current_time = datetime.datetime.now()

        # if movement was detected and then not detected
        # wait 5 seconds to see if there is any more movement
        if has_changed_t2f(movement):
            end_time = current_time + datetime.timedelta(0, 5)

        # Capture frame-by-frame
        ret, frame = capture.read()

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

        # dilate the threshold image to fill in holes, then find contours on thresholded image
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

            movement = True

        if current_time >= end_time:
            break
