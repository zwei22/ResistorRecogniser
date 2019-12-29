import cv2
import numpy as np


class resFinder:
    def __init__(self, cascade_path):
        self.img = None
        self.cascade_model = cv2.CascadeClassifier(cascade_path)

    def find_res(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        resFind = self.cascade_model.detectMultiScale(gray, 1.1, 25)
        return resFind


if __name__ == '__main__':
    finder = resFinder('./cascade.xml')
