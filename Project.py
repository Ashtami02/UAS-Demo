#IMPORTING THE REQUIRED LIBRARIES

import numpy as np
import cv2
import sys
import matplotlib


#WRITING THE CODE FOR LAND AND OCEAN SEGREGATION

l=["1.png","2.png","3.png","4.png","5.png","6.png","7.png","8.png","9.png","10.png"]
for i in l:
    img= cv2.imread(i)
    
    image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) #CONVERT TO HSV
    
    #SETTING THE RANGE OF BLUE COLOR FOR THE OCEAN
    
    lower_ocean = np.array([90, 120, 60])   
    upper_ocean = np.array([120, 255, 150])
    ocean_mask=cv2.inRange(image, lower_ocean, upper_ocean)
    
    #SETTING THE RANGE OF GREEN COLOR FOR THE LAND
    
    lower_land = np.array([40, 120, 80])
    upper_land = np.array([80, 255, 200])
    land_mask=cv2.inRange(image, lower_land, upper_land)
    
    #OVERLAY
    
    copy = img.copy()
    copy[ocean_mask> 0] = [255, 0, 0]    #OCEAN WILL BE REPRESENTED BY BLUE
    copy[land_mask > 0]  = [0, 255, 255]  #LAND WILL BE REPRESENTED BY YELLOW
    
    #TO DISPLAY THE LAND AND OCEAN SEGREGATION
    
    output= f"Overlay_{i}"
    cv2.imwrite(output,copy)
    cv2.imshow("Segmented image",copy)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    #TO GET THE COORDINATES OF RESCUE PADS
    
    grey_image = cv2.cvtColor(copy, cv2.COLOR_BGR2GRAY) #CONVERT TO GRAYSCALE
    grey_image = cv2.medianBlur(grey_image, 5)          #REDUCE NOISE

    #DETECT CIRCLES
    circle = cv2.HoughCircles(
        grey_image,
        cv2.HOUGH_GRADIENT,
        dp=1.2,
        minDist=40,
        param1=100,
        param2=30,
        minRadius=15,
        maxRadius=50
    )

    #STORING THE COORDINATES OF RESCUE PADS
    
    Rescuepads_coordinates = []
    for idx, (x, y, r) in enumerate(circle[0, :], start=1):
        Rescuepads_coordinates.append((x, y, r))
    for i in Rescuepads_coordinates:
        print(i)
        
        
    
                
    
    
    
    