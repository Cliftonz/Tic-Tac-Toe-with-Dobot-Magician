
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


def compare_images(image_a, image_b, title):
    # compute the mean squared error and structural similarity index for the images

    m = mse(image_a, image_b)
    s = ssim(image_a, image_b)

    # setup the figure
    fig = plt.figure()
    plt.suptitle("MSE: %.2f, SSIM: %.2f, Cell: %d" % (m, s, title))

    # show first image
    ax = fig.add_subplot(1, 2, 1)
    cmap = plt.cm.gray
    plt.imshow(image_a, cmap)
    plt.axis("off")

    # show the second image
    ax = fig.add_subplot(1, 2, 2)
    cmap = plt.cm.gray
    plt.imshow(image_b, cmap)
    plt.axis("off")

    # show the images
    plt.show()

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


            # array[i*3 + k] = image[lp1[0] + k * x_block_size: lp1[1] + i * y_block_size,
            #                        lp1[0] + (k + 1) * x_block_size: lp1[1] + (i + 1) * y_block_size]

                # cv2.rectangle(frame,
                #               (lp1[0] + k * x_block_size, lp1[1] + i * y_block_size),
                #               (lp1[0] + (k + 1) * x_block_size, lp1[1] + (i + 1) * y_block_size),
                #               (10 * (i + k), 0 + 10 * (i + k), 0),
                #               inner_thickness)
    # # image_obj[y:y+h, x:x+w]
    # ###################################
    # # Row 1
    #
    # array[0] = image[84:230, 130:290]
    #
    # array[1] = image[84:230, 290:440]
    #
    # array[2] = image[84:230, 450:590]
    # ####################################
    # # Row 2
    #
    # array[3] = image[250:393, 130:290]
    #
    # array[4] = image[250:393, 290:440]
    #
    # array[5] = image[250:393, 450:590]
    # ####################################
    # # Row 3
    #
    # array[6] = image[395:555, 130:280]
    #
    # array[7] = image[395:555, 290:440]
    #
    # array[8] = image[395:555, 450:590]

    return array


def get_player_move(previous_state, current_state):

    previous_cells = set_cells(previous_state)

    current_cells = set_cells(current_state)

    state_to_state_data = [0 for x in range(9)]

    for i in range(0, 9):

        state_to_state_data[i] = compare_images(cv2.cvtColor(previous_cells[i], cv2.COLOR_BGR2GRAY),
                                                cv2.cvtColor(current_cells[i], cv2.COLOR_BGR2GRAY),
                                                str(i))

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

    print("The cell changed is: " + str(get_player_move(previous_state, current_state)))
