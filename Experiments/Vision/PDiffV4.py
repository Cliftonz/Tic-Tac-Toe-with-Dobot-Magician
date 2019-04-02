

from skimage.measure import compare_ssim as ssim
import matplotlib.pyplot as plt
import numpy as np
import cv2
import math
import Vision_Processing as Vision
import time


def mse(image_a, image_b):
    # the 'Mean Squared Error' between the two images is the sum of the squared difference between the two images;
    # NOTE: the two images must have the same dimension
    err = np.sum((image_a.astype("float") - image_b.astype("float")) ** 2)
    err /= float(image_a.shape[0] * image_a.shape[1])

    # return the MSE, the lower the error, the more "similar" the two images are
    #
    return err


def compare_images(image_a, image_b, title, debug):
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


def get_player_move(previous_state, current_state, cam, turn, debug):

    previous_cells = set_cells(previous_state)

    current_cells = set_cells(current_state)

    state_to_state_data = [0 for x in range(9)]

    for i in range(0, 9):

        state_to_state_data[i] = compare_images(cv2.cvtColor(previous_cells[i], cv2.COLOR_BGR2GRAY),
                                                cv2.cvtColor(current_cells[i], cv2.COLOR_BGR2GRAY),
                                                i, debug)

    if debug is True:

        image = [0 for x in range(9)]

        for i in range(0, 9):
            image[i] = np.hstack((previous_cells[i], current_cells[i]))

            image[i] = cv2.resize(image[i], (600, 300))

            cv2.putText(image[i], "Cell: {} mse: {} simm: {}".format(str(i),state_to_state_data[0], state_to_state_data[1]), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)



        while True:
            # grab the current frame and initialize the occupied/unoccupied text
            if not (cam.grab()):
                print("No more frames")
                break

            cells1 = np.hstack((np.vstack((image[0], image[1])), np.vstack((image[2], image[3]))))

            cells2 = np.hstack((np.vstack((image[4], image[5])), np.vstack((image[6], image[7]))))

            cells3 = np.hstack((image[8], image[8]))

            final_image = np.vstack((cells1, cells2, cells3))

            cv2.imshow('cells', final_image)

            key = cv2.waitKey(1)

            # if the `q` key is pressed, break from the lop
            if key == ord("q") or key == 13:
                cv2.destroyAllWindows()
                break

    return find_player_move(state_to_state_data)


if __name__ == '__main__':
    # load the images -- the previous, the previous + current,
    # and the previous + photoshop

    cam = cv2.VideoCapture(0)

    Vision.camera_overlay(cam)

    flags, previous_state = cam.read()

    print("Letter:")
    choice = input().lower()

    flags, current_state = cam.read()

    print("The cell changed is: " + str(get_player_move(previous_state, current_state, cam, 1, True)))
