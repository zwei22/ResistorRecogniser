import cv2
import numpy as np

from resFinder import *


def main():

    cap = cv2.VideoCapture(1)
    finder = resFinder()

    while True:
        ret, frame = cap.read()
        res = finder.find_res(frame)
        # for r in res:
        #     reader = resReader()
            


        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
