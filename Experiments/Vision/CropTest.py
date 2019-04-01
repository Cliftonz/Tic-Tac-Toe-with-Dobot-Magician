
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


if __name__ == '__main__':
    
    # load the images -- the previous, the previous + current,
    # and the previous + photoshop
    previous = cv2.imread("TestData/t0.jpg")
    current = cv2.imread("TestData/t1.jpg")

    PreviousCells = [0 for x in range(9)]

    CurrentCells = [0 for x in range(9)]

    # previous[lp1[1]:(lp1[1] + LYBlockSize), lp1[0]:(lp1[0] + LXBlockSize)]
    # image_obj[ y:y+h, x:x+w]
    ###################################
    # Row 1
    ###################################
    PreviousCells[0] = previous[84:230, 130:290]

    PreviousCells[1] = previous[84:230, 290:440]

    PreviousCells[2] = previous[84:230, 450:590]
    ####################################
    # Row 2
    ####################################
    PreviousCells[3] = previous[250:393, 130:290]

    PreviousCells[4] = previous[250:393, 290:440]

    PreviousCells[5] = previous[250:393, 450:590]
    ####################################
    # Row 3
    ####################################
    PreviousCells[6] = previous[395:555, 130:280]

    PreviousCells[7] = previous[395:555, 290:440]

    PreviousCells[8] = previous[395:555, 450:590]

    ###################################
    # Row 1
    ###################################
    CurrentCells[0] = current[84:230, 130:290]

    CurrentCells[1] = current[84:230, 290:440]

    CurrentCells[2] = current[84:230, 450:590]
    ####################################
    # Row 2
    ####################################
    CurrentCells[3] = current[250:393, 130:290]

    CurrentCells[4] = current[250:393, 290:440]

    CurrentCells[5] = current[250:393, 450:590]
    ####################################
    # Row 3
    ####################################
    CurrentCells[6] = current[395:555, 130:280]

    CurrentCells[7] = current[395:555, 290:440]

    CurrentCells[8] = current[395:555, 450:590]

    ComData = [0 for x in range(9)]
    
    for i in range(0, 9):
        title = 'Cell ' + str(i)
        ComData[i] = compare_images(cv2.cvtColor(PreviousCells[i], cv2.COLOR_BGR2GRAY), 
                                    cv2.cvtColor(CurrentCells[i], cv2.COLOR_BGR2GRAY),
                                    title)
        
    print(ComData)
    
    playerMove = find_player_move(ComData)
    
    print(playerMove)
