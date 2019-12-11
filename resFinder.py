import cv2
import numpy as np


class resFinder:
    def __init__(self):
        self.img = None

    def find_res(self, img):

        # img = cv2.GaussianBlur(img, (7, 7), 0)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # hsv_lower = np.array([0,0,0])
        # hsv_upper = np.array([40,80,255])
        # mask = cv2.inRange(hsv, hsv_lower, hsv_upper)

        # res = cv2.bitwise_and(img,img, mask= mask)
        thresh = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,31,10)
        # thresh = cv2.erode(thresh,(3,3),iterations=7)
        # thresh = cv2.dilate(thresh,(3,3),iterations=7)
        # thresh = cv2.dilate(thresh,(3,3),iterations=7)
        # thresh = cv2.erode(thresh,(3,3),iterations=7)

        
        # ret, thresh = cv2.threshold(gray, 60, 255, 0)
        # thresh = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,11,2)
        # thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, (7,7))
        # thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, (7,7))
        cv2.imshow('th',thresh)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        

        for i, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if 100<area<10000:
                cv2.drawContours(img, contours, i, (0,255,0), 3)
                print(area, end='\t')
        # print('')
        


        # image = np.hstack([img, cv2.bitwise_and(img,img, mask= mask)])
        # cv2.imshow('frame', image)



if __name__ == '__main__':
    pass
