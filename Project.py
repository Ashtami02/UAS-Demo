#IMPORTING THE REQUIRED LIBRARIES


import numpy as np
import cv2
import sys
import matplotlib


#WRITING THE CODE FOR LAND AND OCEAN SEGREGATION

l=["1.png","2.png","3.png","4.png","5.png","6.png","7.png","8.png","9.png","10.png"]
for i in l:
    img= cv2.imread(i)
    cv2.imshow("image",img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    

