import cv2
import numpy as np
import argparse

def nothing(x):
    pass

cap = cv2.VideoCapture(0)

x_center = 320
y_center = 240

center_deviation = 5

alpha = 0.4
beta = 1 - alpha

new_coordinates = 0
old_coordinates = None



cv2.namedWindow('image')

cv2.createTrackbar('DownH1','image', 65, 255, nothing)
cv2.createTrackbar('UpH1','image', 80, 255, nothing)

cv2.createTrackbar('DownS','image', 0, 255, nothing)
cv2.createTrackbar('UpS','image', 255, 255, nothing)

cv2.createTrackbar('DownV','image', 0, 255, nothing)
cv2.createTrackbar('UpV','image', 255, 255, nothing)

cv2.createTrackbar('erosion','image', 3, 20, nothing)
cv2.createTrackbar('dilation','image', 3, 20, nothing)

cv2.createTrackbar('minrad','image', 3, 255, nothing)
cv2.createTrackbar('maxrad','image', 700, 1000, nothing)

cv2.createTrackbar('deviation','image', 0, 240, nothing)

x = None
y = None

while(1):



    DownH1 = cv2.getTrackbarPos('DownH1','image')
    UpH1 = cv2.getTrackbarPos('UpH1','image')

    DownS = cv2.getTrackbarPos('DownS','image')
    UpS = cv2.getTrackbarPos('UpS','image')

    DownV = cv2.getTrackbarPos('DownV','image')
    UpV = cv2.getTrackbarPos('UpV','image')

    erosion_iter = cv2.getTrackbarPos('erosion','image')
    dilation_iter = cv2.getTrackbarPos('dilation','image')

    minrad = cv2.getTrackbarPos('minrad','image')
    maxrad = cv2.getTrackbarPos('maxrad','image')

    center_deviation = cv2.getTrackbarPos('deviation','image')

    x_right_deviation = x_center + center_deviation
    x_left_deviation = x_center - center_deviation
    y_up_deviation = y_center - center_deviation
    y_down_deviation = y_center + center_deviation

    _, frame = cap.read()
    output = frame.copy()


    blur = cv2.GaussianBlur(frame,(5,5),0)
   
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

    lower_value = np.array([DownH1,DownS,DownV])
    upper_value = np.array([UpH1,UpS,UpV])
    res = cv2.inRange(hsv, lower_value, upper_value)


    kernel = np.ones((5,5), np.uint8)

    erosion = cv2.erode(res, kernel, iterations = erosion_iter)

    opening = cv2.morphologyEx(erosion, cv2.MORPH_OPEN, kernel)

    dilation = cv2.dilate(erosion, kernel, iterations = dilation_iter)

    processed = cv2.bitwise_and(frame,frame, mask = dilation)




    #create circle
    gray = cv2.cvtColor(processed, cv2.COLOR_BGR2GRAY)

    #circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1.2, 100)
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, minrad, maxrad)

    if circles is not None:
    # convert the (x, y) coordinates and radius of the circles to integers
        
        circles = np.round(circles[0, :]).astype("int")
 
    # loop over the (x, y) coordinates and radius of the circles
        for (x, y, r) in circles:
            
            new_coordinates = np.array([x, y, r])
            
            if old_coordinates is None:
                old_coordinates = new_coordinates

            valid_coordinates = new_coordinates * alpha + old_coordinates * beta

            old_coordinates = new_coordinates

            x = int(valid_coordinates[0])
            y = int(valid_coordinates[1])
            r = int(valid_coordinates[2])
            # draw the circle in the output image, then draw a rectangle
            # corresponding to the center of the circle
            cv2.circle(output, (x, y), r, (0, 255, 0), 4)
            cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)

            # cv2.circle(output, (valid_coordinates[0], valid_coordinates[1]), valid_coordinates[2], (0, 255, 0), 4)
            # cv2.rectangle(output, (valid_coordinates[0] - 5, valid_coordinates[1] - 5), (valid_coordinates[0] + 5, valid_coordinates[1] + 5), (0, 128, 255), -1)

    if (x or y) is not None:
       
        if valid_coordinates[0] > x_right_deviation or valid_coordinates[0] < x_left_deviation or valid_coordinates[1] < y_up_deviation or valid_coordinates[1] >y_down_deviation:

            if x > x_right_deviation:
                print('deviation to the right x')
            
            if x < x_left_deviation:
                print('deviation to the left x')

            if y < y_up_deviation:
                print('upward deviation y')
            
            if y > y_down_deviation:
                print('downward deviation y')
        
        else: print('good')        
        

    else: print('not found x or y')



    

    




    cv2.imshow('image',output )
    cv2.imshow('frame', dilation)
    cv2.imshow('original', frame)
    cv2.imshow('circle', processed)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()