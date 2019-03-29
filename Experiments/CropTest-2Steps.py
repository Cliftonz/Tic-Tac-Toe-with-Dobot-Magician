from skimage.measure import compare_ssim as ssim
import matplotlib.pyplot as plt
import numpy as np
import cv2


def mse(image_a, image_b):
    # the 'Mean Squared Error' between the two images is the
    # sum of the squared difference between the two images;
    # NOTE: the two images must have the same dimension
    err = np.sum((image_a.astype("float") - image_b.astype("float")) ** 2)
    err /= float(image_a.shape[0] * image_a.shape[1])

    # return the MSE, the lower the error, the more "similar"
    # the two images are
    return err


def compare_images(image_a, image_b, title):
    # compute the mean squared error and structural similarity
    # index for the images
    m = mse(image_a, image_b)
    s = ssim(image_a, image_b)

    # setup the figure
    fig = plt.figure(title)
    plt.suptitle("MSE: %.2f, SSIM: %.2f" % (m, s))

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
    # one is the largest the ssim can be
    smallest_s = 1
    for k in range(0, 8):
        if largest_m < compared_value[k][0] and smallest_s > compared_value[k][1]:
            largest_m = compared_value[k][0]
            smallest_s = compared_value[k][1]
            position = k + 1

    return position


def set_cells(image):
    """Takes an image and crops the image based on a set of pixels that defines the edges of the box."""

    array = [0 for x in range(9)]

    # image_obj[ y:y+h, x:x+w]
    ###################################
    # Row 1
    ###################################
    array[0] = image[84:230, 130:290]

    array[1] = image[84:230, 290:440]

    array[2] = image[84:230, 450:590]
    ####################################
    # Row 2
    ####################################
    array[3] = image[250:393, 130:290]

    array[4] = image[250:393, 290:440]

    array[5] = image[250:393, 450:590]
    ####################################
    # Row 3
    ####################################
    array[6] = image[395:555, 130:280]

    array[7] = image[395:555, 290:440]

    array[8] = image[395:555, 450:590]

    return array


if __name__ == '__main__':

    # load the images -- the previous, the previous + current,
    # and the previous + photoshop
    previous = cv2.imread("TestData/t0.jpg")
    current = cv2.imread("TestData/t1.jpg")
    future = cv2.imread("TestData/t2.jpg")

    PreviousCells = set_cells(previous)

    CurrentCells = set_cells(current)

    FutureCells = set_cells(future)

    ComData = [0 for x in range(9)]

    for i in range(0, 9):
        title = 'Cell ' + str(i)
        ComData[i] = compare_images(cv2.cvtColor(PreviousCells[i], cv2.COLOR_BGR2GRAY),
                                    cv2.cvtColor(CurrentCells[i], cv2.COLOR_BGR2GRAY),
                                    title)

    print(ComData)

    playerMove = find_player_move(ComData)

    print("The move made is " + str(playerMove))

    for i in range(0, 9):
        title = 'Cell ' + str(i)
        ComData[i] = compare_images(cv2.cvtColor(CurrentCells[i], cv2.COLOR_BGR2GRAY),
                                    cv2.cvtColor(FutureCells[i], cv2.COLOR_BGR2GRAY),
                                    title)

    print(ComData)

    playerMove = find_player_move(ComData)

    print("The move made is " + str(playerMove))
