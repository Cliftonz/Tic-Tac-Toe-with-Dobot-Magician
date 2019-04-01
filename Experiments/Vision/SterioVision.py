
import cv2

if __name__ == '__main__':
    left = cv2.VideoCapture(0)
    right = cv2.VideoCapture(1)



    left.release()
    while(True):
        if not (left.grab() and right.grab()):
            print("No more frames")
            break

        _, leftFrame = left.retrieve()
        _, rightFrame = right.retrieve()

        cv2.imshow('left', leftFrame)
        cv2.imshow('right', rightFrame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    right.release()
    cv2.destroyAllWindows()