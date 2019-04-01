
from skimage.measure import compare_ssim as ssim
import matplotlib.pyplot as plt
import numpy as np
import cv2
import math


# https://www.pyimagesearch.com/2014/09/15/python-compare-two-images/

def mse(imageA, imageB):
    # the 'Mean Squared Error' between the two images is the
    # sum of the squared difference between the two images;
    # NOTE: the two images must have the same dimension
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])

    # return the MSE, the lower the error, the more "similar"
    # the two images are
    return err


def compare_images(imageA, imageB, title):
    # compute the mean squared error and structural similarity
    # index for the images
    m = mse(imageA, imageB)
    s = ssim(imageA, imageB)

    # setup the figure
    fig = plt.figure(title)
    plt.suptitle("MSE: %.2f, SSIM: %.2f" % (m, s))

    # show first image
    ax = fig.add_subplot(1, 2, 1)
    cmap = plt.cm.gray
    plt.imshow(imageA, cmap)
    plt.axis("off")

    # show the second image
    ax = fig.add_subplot(1, 2, 2)
    cmap = plt.cm.gray
    plt.imshow(imageB, cmap)
    plt.axis("off")

    # show the images
    plt.show()


if __name__ == '__main__':
    # load the images -- the previous, the previous + current,
    # and the previous + photoshop
    previous = cv2.imread("TestData/t0.jpg")
    current = cv2.imread("TestData/t1.jpg")

    lp1 = (29, 82)
    lp2 = (299, 350)

    LXBlockSize = math.ceil((lp2[0] - lp1[0]) / 3)

    LYBlockSize = math.ceil((lp2[1] - lp1[1]) / 3)

    # cut image up, Store image, convert the images to grayscale
    PreviousCells = [0 for x in range(10)]

    CurrentCells = [0 for x in range(10)]
    
    for i in range(0, 9):
        PreviousCells[i] = cv2.cvtColor(previous[lp1[1]:(lp1[1] + LYBlockSize), lp1[0]:(lp1[0] + LXBlockSize)], cv2.COLOR_BGR2GRAY)

    for i in range(0, 9):
        CurrentCells[i] = cv2.cvtColor(current[lp1[1]:(lp1[1] + LYBlockSize), lp1[0]:(lp1[0] + LXBlockSize)], cv2.COLOR_BGR2GRAY)

    # initialize the figure
    fig = plt.figure("Images")
    images = ("Previous", PreviousCells[1]), ("Current", CurrentCells[0])

    # loop over the images
    for (i, (name, image)) in enumerate(images):
        # show the image
        ax = fig.add_subplot(1, 3, i + 1)
        ax.set_title(name)
        cmap = plt.cm.gray
        plt.imshow(image, cmap)
        plt.axis("off")

    # show the figure
    plt.show()

    # compare the images
    compare_images(previous[0], previous[0], "previous c1 vs. previous c1")
    compare_images(previous[0], current[0], "previous c1 vs. current c1")
