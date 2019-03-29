from skimage.measure import compare_ssim as ssim
import matplotlib.pyplot as plt
import numpy as np
import cv2


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
    # load the images -- the original, the original + MoveAdded,
    # and the original + photoshop
    original = cv2.imread("TestData/t0.jpg")
    MoveAdded = cv2.imread("TestData/t1.jpg")

    # convert the images to grayscale
    original = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
    MoveAdded = cv2.cvtColor(MoveAdded, cv2.COLOR_BGR2GRAY)

    # initialize the figure
    fig = plt.figure("Images")
    images = ("Previous", original), ("Current", MoveAdded)

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
    compare_images(original, original, "Original vs. Original")
    compare_images(original, MoveAdded, "Original vs. MoveAdded")
