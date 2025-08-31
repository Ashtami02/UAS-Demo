#IMPORTING THE REQUIRED LIBRARIES

import numpy as np
import cv2
import sys
import matplotlib
import math

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
    copy[ocean_mask> 0] = [255, 0, 0]     #OCEAN WILL BE REPRESENTED BY BLUE
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
    circle = cv2.HoughCircles(grey_image, cv2.HOUGH_GRADIENT, dp=1.2, minDist=30, param1=100, param2=18, minRadius=15, maxRadius=60)
    pad_colors = {
        "white":  [(0, 0, 200), (180, 40, 255)],    
        "light_blue": [(85, 50, 180), (110, 150, 255)],  
        "pink":  [(135, 50, 180), (150, 150, 255)]   
    }

    #STORING THE COORDINATES OF RESCUE PADS
    
    rescue_pads = []
    if circle is not None:
        circle = np.uint16(np.around(circle))

        for (x, y, r) in circle[0, :]:
            #GET HSV VALUE OF THE PAD
            h, s, v = image[y, x]

            #TO AVOID ANY FALSE CIRCLES AND TO ONLY DETECT RESCUE PADS
            is_pad = False
            for lower, upper in pad_colors.values():
                lower = np.array(lower)
                upper = np.array(upper)
                if np.all(image[y, x] >= lower) and np.all(image[y, x] <= upper):
                    is_pad = True
                    break
            if is_pad:
                rescue_pads.append((x, y))
    
    #CREATING A DICTIONARY OF THE RANGE OF COLORS FOR THE CASUALTIES
    
    Color={"red": [([0, 50, 200], [10, 255, 255]),([170, 50, 200], [179, 255, 255])],
           "yellow": [(20, 100, 100), (35, 255, 255)],
           "green": [(40, 50, 50), (80, 255, 255)],}
    
    
    Casualities_info = []
    
    for key,value in Color.items():
        if key== "red":             #CREATING A SEPERATE MASK FOR RED

            lower1, upper1 = value[0]
            lower2, upper2 = value[1]

            mask1 = cv2.inRange(image, np.array(lower1), np.array(upper1))
            mask2 = cv2.inRange(image, np.array(lower2), np.array(upper2))
            mask = cv2.bitwise_or(mask1, mask2)
        else:
        
            mask = cv2.inRange(image, np.array(value[0]), np.array(value[1]))            #CREATING A BINARY MASK

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #GETTING THE BOUNDARY
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area < 20 or area > 8000:
                continue

            #TO GET THE COORDINATES OF CASUALITIES
            
            x, y, w, h = cv2.boundingRect(cnt)
            X, Y = x + w // 2, y + h // 2
            
            #DETECTING THE SHAPE OF THE CASUALITIES
            
            approx = cv2.approxPolyDP(cnt, 0.04 * cv2.arcLength(cnt, True), True)
            if len(approx) == 3:
                shape = "Triangle"
            elif len(approx) == 4:
                shape = "square"
            else:
                shape = "Star"
                
            #STORING INFORMATION REGARDING THE CASUALITIES
            
            l=[X,Y,key,shape]
            Casualities_info.append(l)

    '''print(i," → Casualties found: ",len(Casualities_info))'''
    
    #CREATING THE DISTANCE MATRIX
    
    distance_matrix = []
    for c in (Casualities_info):
        casualty_distances = []

        for padindex, pad in enumerate(rescue_pads, start=1):
            d = math.sqrt((pad[0] - c[0]) ** 2 + (pad[1] - c[1]) ** 2)       #APPLYING THE DISTANCE FORMULA 
            casualty_distances.append((f"Pad {padindex}", round(d, 2)))

        distance_matrix.append({
            "position": (c[0], c[1]),
            "color": c[2],
            "shape": c[3],
            "distances": casualty_distances
        })

    # PRINT DISTANCE MATRIX 
    
    for b in distance_matrix:
        print(i,"Casualty", ({b['color']}, {b['shape']}),"at", {b['position']})
        for pad, dist in b["distances"]:
            print( "Distance to ",pad, dist)
    
