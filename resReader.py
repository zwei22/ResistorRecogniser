import cv2
import numpy as np

COLOUR_BOUNDS = [
                [(0, 0, 0)   , (179, 50, 65)  , "BLACK"  , 0 , (0,0,0)       ],    
                [(0, 65, 45)    , (13, 170, 95)  , "BROWN"  , 1 , (0,51,102)    ],    
                [(0, 168, 50)    , (10, 255, 150)  , "RED"    , 2 , (0,0,255)     ],
                [(12, 145, 73)   , (20, 255, 200)  , "ORANGE" , 3 , (0,128,255)   ], 
                [(21, 160, 125) , (30, 255, 255)  , "YELLOW" , 4 , (0,255,255)   ],
                [(60, 30, 30)  , (95, 90, 95)   , "GREEN"  , 5 , (0,255,0)     ],  
                [(105, 125, 40)    , (114, 255, 150)  , "BLUE"   , 6 , (255,0,0)     ],  
                [(115, 40, 37) , (135, 100, 100) , "PURPLE" , 7 , (255,0,127)   ], 
                [(0, 0, 70)     , (179, 50, 200)   , "GRAY"   , 8 , (128,128,128) ],      
                [(0, 0, 200)     , (179, 10, 255)  , "WHITE"  , 9 , (255,255,255) ],
                ]
RED_TOP_LOWER = (160, 30, 80)
RED_TOP_UPPER = (179, 255, 200)
MIN_AREA = 700
FONT = cv2.FONT_HERSHEY_SIMPLEX

class resReader:
   
    def __init__(self, img):
        self.img = img
        self.pos = (0, 0, len(self.img[0]),len(self.img))

    def validContour(self, cnt):
        #looking for a large enough area and correct aspect ratio
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
        img_bil = cv2.bilateralFilter(self.img,5,80,80)
        hsv = cv2.cvtColor(img_bil, cv2.COLOR_BGR2HSV)

        thresh = cv2.adaptiveThreshold(cv2.cvtColor(img_bil, cv2.COLOR_BGR2GRAY),255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,59,5)
        thresh = cv2.bitwise_not(thresh)

        bandsPos = []

        checkColours = COLOUR_BOUNDS

        for clr in checkColours:
            mask = cv2.inRange(hsv, clr[0], clr[1])

            if (clr[2] == "RED"): #combining the 2 RED ranges in hsv

                redMask2 = cv2.inRange(hsv, RED_TOP_LOWER, RED_TOP_UPPER)
                mask = cv2.bitwise_or(redMask2,mask,mask)                

            mask = cv2.bitwise_and(mask,thresh,mask= mask)
            contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            #filter invalid contours, store valid ones
            for k in range(len(contours)-1,-1,-1):
                #print(contours)
                if (self.validContour(contours[k])):
                    leftmostPoint = tuple(contours[k][contours[k][:,:,0].argmin()][0])
                    bandsPos += [leftmostPoint + tuple(clr[2:])]
                    cv2.circle(img_bil, leftmostPoint, 5, (255,0,255),-1)
                else:
                    contours.pop(k)
            
            cv2.drawContours(img_bil, contours, -1, clr[-1], 3)
                              
        cv2.imshow('Contour Display', img_bil)#shows the most recent resistor checked.

        #sort by 1st element of each tuple and return
        return sorted(bandsPos, key=lambda tup: tup[0])

    def read_value(self, sortedBands, liveimg):
        x,y,w,h = self.pos

        strVal = ""

        if (len(sortedBands) in [3,4,5]):
            for band in sortedBands[:-1]:
                strVal += str(band[3])

            intVal = int(strVal)
            intVal *= 10**sortedBands[-1][3]

            cv2.rectangle(liveimg,(x,y),(x+w,y+h),(0,255,0),2)

            cv2.putText(liveimg,str(intVal) + " OHMS",(x,y+int(h/2)), FONT, 1,(255,255,255),2,cv2.LINE_AA)

            return
        #draw a red rectangle indicating an error reading the bands
        cv2.rectangle(liveimg,(x,y),(x+w,y+h),(0,0,255),2)

    def print_result(self):
        pass


if __name__=='__main__':
    #r = resReader()
    img = cv2.imread('figures/2.5k_1_res.jpg')
    reader = resReader(img)

    while(not (cv2.waitKey(1) == ord('q'))):
        sorted_band = reader.read_band()
        reader.read_value(sorted_band, img)

        cv2.imshow("Frame",img)
    #cap.release()
    cv2.destroyAllWindows()
