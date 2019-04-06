from skimage.measure import compare_ssim as ssim
import numpy as np
import cv2
import math


def mse(image_a, image_b):
    # the 'Mean Squared Error' between the two images is the sum of the squared difference between the two images;
    # NOTE: the two images must have the same dimension
    err = np.sum((image_a.astype("float") - image_b.astype("float")) ** 2)
    err /= float(image_a.shape[0] * image_a.shape[1])

    # return the MSE, the lower the error, the more "similar" the two images are
    #
    return err


def compare_images(image_a, image_b):
    # compute the mean squared error and structural similarity index for the images

    m = mse(image_a, image_b)
    s = ssim(image_a, image_b)

    return m, s


def find_player_move(compared_value):

    largest_m = 0
    smallest_s = 1

    for k in range(0, 9):
        if largest_m < compared_value[k][0] and smallest_s > compared_value[k][1]:

            largest_m = compared_value[k][0]
            smallest_s = compared_value[k][1]
            position = k + 1

    return position


def set_cells(image):
    """Takes an image and crops the image based on a set of pixels that defines the edges of the box."""

    array = [0 for x in range(9)]

    lp1 = (29, 82)
    lp2 = (299, 350)

    x_block_size = math.ceil((lp2[0] - lp1[0]) / 3)

    y_block_size = math.ceil((lp2[1] - lp1[1]) / 3)

    for i in range(0, 3):
        for k in range(0, 3):
            array[i * 3 + k] = image[lp1[1] + i * y_block_size: lp1[1] + (i + 1) * y_block_size,
                                     lp1[0] + k * x_block_size: lp1[0] + (k + 1) * x_block_size]

    return array


def get_player_move(previous_state, current_state, debug, file):

    previous_cells = set_cells(previous_state)

    current_cells = set_cells(current_state)

    state_to_state_data = [0 for x in range(9)]

    for i in range(0, 9):

        state_to_state_data[i] = compare_images(cv2.cvtColor(previous_cells[i], cv2.COLOR_BGR2GRAY),
                                                cv2.cvtColor(current_cells[i], cv2.COLOR_BGR2GRAY))

    if debug is True:

        image = [0 for x in range(9)]

        for i in range(0, 9):
            image[i] = np.hstack((previous_cells[i], current_cells[i]))

            image[i] = cv2.resize(image[i], (550, 250))

            cv2.putText(image[i], "Cell: {} mse: {} simm: {}".format(str(i),
                                                                     state_to_state_data[i][0],
                                                                     state_to_state_data[i][1]),
                        (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        # file.write(find_player_move(state_to_state_data))

    return find_player_move(state_to_state_data)


def camera_overlay(capture):

    inner_thickness = 1

    rp1 = (360, 83)
    rp2 = (635, 355)

    lp1 = (29, 82)
    lp2 = (299, 350)

    x_block_size = math.ceil((lp2[0] - lp1[0]) / 3)

    y_block_size = math.ceil((lp2[1] - lp1[1]) / 3)

    while True:
        if not (capture.grab()):
            print("No more frames")
            break
        # Capture frame-by-frame
        ret, frame = capture.read()

        line_thickness = 2

        # right square
        cv2.rectangle(frame, rp1, rp2, (0, 255, 0), line_thickness)

        # left square
        cv2.rectangle(frame, lp1, lp2, (255, 0, 0), line_thickness)

        for i in range(0, 3):
            for k in range(0, 3):
                cv2.rectangle(frame,
                              (lp1[0] + k * x_block_size, lp1[1] + i * y_block_size),
                              (lp1[0] + (k + 1) * x_block_size, lp1[1] + (i + 1) * y_block_size),
                              (10 * (i + k), 0 + 10 * (i + k), 0),
                              inner_thickness)

        # Adding text

        font = cv2.FONT_HERSHEY_SIMPLEX
        start_of_text = (10, 50)
        font_scale = 1
        font_color = (255, 255, 255)
        line_type = 2

        cv2.putText(frame, 'Press \'q\' once position is finalized.',
                    start_of_text,
                    font,
                    font_scale,
                    font_color,
                    line_type)

        # Display the resulting frame
        cv2.imshow('video', frame)

        c = cv2.waitKey(1)

        if c == 27 or c == 113:
            break

    cv2.destroyAllWindows()
