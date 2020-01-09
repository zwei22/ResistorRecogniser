import cv2
import numpy as np

COLOUR_BOUNDS = [
                [(0, 0, 8)     , (179, 66, 31)  , "BLACK"  , 0 , (0,0,0)       ],    
                [(5, 94, 30)   , (13, 199, 103) , "BROWN"  , 1 , (0,51,102)    ],    
                [(0, 178, 71)  , (5, 225, 138)  , "RED"    , 2 , (0,0,255)     ],
                [(7, 186, 77)  , (13, 235, 187) , "ORANGE" , 3 , (0,128,255)   ], 
                [(21, 160, 125), (30, 255, 255) , "YELLOW" , 4 , (0,255,255)   ],
                [(40, 26, 12)  , (100, 149, 50) , "GREEN"  , 5 , (0,255,0)     ],  
                [(105, 12, 45) , (113, 107, 131), "BLUE"   , 6 , (255,0,0)     ],  
                [(121, 25, 61) , (160, 60, 126) , "PURPLE" , 7 , (255,0,127)   ], 
#               [(0, 0, 70)    , (179, 50, 200) , "GRAY"   , 8 , (128,128,128) ],      
                [(0, 0, 200)   , (179, 10, 255) , "WHITE"  , 9 , (255,255,255) ],
                ]
RED_TOP_LOWER = (160, 30, 80)
RED_TOP_UPPER = (179, 255, 200)
MIN_AREA = 700
FONT = cv2.FONT_HERSHEY_SIMPLEX

class resReader:
   
    def __init__(self):
        pass

    def read_img(self, img):
        self.img = img
        self.pos = (0, 0, self.img.shape[1], self.img.shape[0])

    def validContour(self, cnt):
        if(cv2.contourArea(cnt) < MIN_AREA):
            return False
        else:
            x,y,w,h = cv2.boundingRect(cnt)
            aspectRatio = float(w)/h
            if (aspectRatio > 0.4):
                return False
        return True

    def read_band(self):
        resImg = cv2.resize(self.img, (400, 200))
        img_bil = cv2.bilateralFilter(resImg,5,80,80)
        hsv = cv2.cvtColor(img_bil, cv2.COLOR_BGR2HSV)

        thresh = cv2.adaptiveThreshold(cv2.cvtColor(img_bil, cv2.COLOR_BGR2GRAY),255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,59,5)
        thresh = cv2.bitwise_not(thresh)

        bandsPos = []

        checkColours = COLOUR_BOUNDS

        for clr in checkColours:
            mask = cv2.inRange(hsv, clr[0], clr[1])

            if (clr[2] == "RED"):

                redMask2 = cv2.inRange(hsv, RED_TOP_LOWER, RED_TOP_UPPER)
                mask = cv2.bitwise_or(redMask2,mask,mask)               

            mask = cv2.bitwise_and(mask,thresh,mask= mask)
            contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            #filter invalid contours, store valid ones
            for k in range(len(contours)-1,-1,-1):
                if (self.validContour(contours[k])):
                    leftmostPoint = tuple(contours[k][contours[k][:,:,0].argmin()][0])
                    bandsPos += [leftmostPoint + tuple(clr[2:])]
                    cv2.circle(img_bil, leftmostPoint, 5, (255,0,255),-1)
                else:
                    contours.pop(k)
            
            cv2.drawContours(img_bil, contours, -1, clr[-1], 3)
        cv2.imshow('Test mask', mask)             
        cv2.imshow('Contour Display', img_bil)

        return sorted(bandsPos, key=lambda tup: tup[0])

    def read_value(self, sortedBands, liveimg):
        x,y,w,h = self.pos

        strVal = ""

        if (len(sortedBands) in [3,4,5]):
            color = []
            for band in sortedBands: 
                color.append(band[3])

            unit = ['','k','M','G']
            #color = self.color_value
            q, r = divmod(color[2]+1,3)
            value = round((1*color[0]+0.1*color[1])*pow(10,r),1)
            return str(value)+unit[q]+'OHM'
        else:
            return ""

    def print_result(self, result):
        print(result)


if __name__=='__main__':
    #r = resReader()
    img = cv2.imread('figures/test.jpg')
    reader = resReader()
    reader.read_img(img)
    while(not (cv2.waitKey(1) == ord('q'))):
        sorted_band = reader.read_band()
        result = reader.read_value(sorted_band, img)
        reader.print_result(result)
        #cv2.imshow("Frame",img)
    #cap.release()
    cv2.destroyAllWindows()
