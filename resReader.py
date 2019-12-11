import cv2
import numpy as np

COLOUR_BOUNDS = [
                [(0, 0, 0)      , (179, 255, 93)  , "BLACK"  , 0 , (0,0,0)       ],    
                [(0, 90, 10)    , (15, 250, 100)  , "BROWN"  , 1 , (0,51,102)    ],    
                [(0, 30, 80)    , (10, 255, 200)  , "RED"    , 2 , (0,0,255)     ],
                [(10, 70, 70)   , (25, 255, 200)  , "ORANGE" , 3 , (0,128,255)   ], 
                [(30, 170, 100) , (40, 250, 255)  , "YELLOW" , 4 , (0,255,255)   ],
                [(35, 20, 110)  , (60, 45, 120)   , "GREEN"  , 5 , (0,255,0)     ],  
                [(65, 0, 85)    , (115, 30, 147)  , "BLUE"   , 6 , (255,0,0)     ],  
                [(120, 40, 100) , (140, 250, 220) , "PURPLE" , 7 , (255,0,127)   ], 
                [(0, 0, 50)     , (179, 50, 80)   , "GRAY"   , 8 , (128,128,128) ],      
                [(0, 0, 90)     , (179, 15, 250)  , "WHITE"  , 9 , (255,255,255) ],
                ]

class resReader:

    def __init__(self):
        self.img = None
        self.res_img = None
        self.pos = (0, 0, 0, 0)
        self.color_value = []
        self.value_str = ""

    def read_img(self, img, pos):
        # img: original frame from camera
        # pos: tuple (x, y, w, h)
        x, y, w, h = pos
        self.img = img
        self.res_img = img[x:x+w, y:y+h]    

    def read_band(self, img):
        img = cv2.bilateralFilter(img,5,80,80)
        # img = cv2.GaussianBlur(img, (7, 7), 0)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        thresh = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,59,5)
        
        
        # thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, (7,7))
        # edges = cv2.Canny(gray,50,200)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for i, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if 10<area<1000:
                cv2.drawContours(img, contours, i, (0,255,0), 1)
        cv2.imshow('a',img)


        # cv2.imshow('1',thresh)
        cv2.waitKey(1)
        cv2.destroyAllWindows()

    def read_value(self):
        unit = ['','k','M','G']
        color = self.color_value
        q, r = divmod(color[2]+1,3)
        value = round((1*color[0]+0.1*color[1])*pow(10,r),1)
        self.value_str = str(value)+unit[q]+'Ω'
        return self.value_str

    def print_result(self):
        # return image with label
        #cv2.puttext
        pass

if __name__=='__main__':
    r = resReader()
    img = cv2.imread('1k.png')
    # r.color_value = [3,3,2]
    # print(r.read_value())

    r.read_band(img)