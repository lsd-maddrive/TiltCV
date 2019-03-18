import cv2
import image_processing as ip
import numpy as np



def finding_a_circle_around_the_contour(frame):

	dilation = ip.processing_morphological_operators(frame)

	x = None
	y = None
	# _, contours, hierarchy = cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	contours,_ = cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

	cv2.drawContours(frame,contours,0,(0,0,255),2)
	
	if contours:

		cnt = contours[0]
		(x,y), radius = cv2.minEnclosingCircle(cnt)
		center = (int(x),int(y))
		radius = int(radius)

		cv2.circle(frame,center,radius,(0,255,0),2)

	return frame, x,y



def Hough_circle(output,minrad,maxrad):
		
		#create circle
    dilation = ip.processing_morphological_operators(output)

    circles = cv2.HoughCircles(dilation, cv2.HOUGH_GRADIENT, minrad, maxrad)
    
    if circles is not None:
    # convert the (x, y) coordinates and radius of the circles to integers      
        circles = np.round(circles[0, :]).astype("int")
 
    # loop over the (x, y) coordinates and radius of the circles
        for (x, y, r) in circles:
            cv2.circle(output, (x, y), r, (0, 255, 0), 4)
            cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)


def Hough_circle_v2(frame,dp,minDist,param1,param2,minRadius,maxRadius):
	circles = cv2.HoughCircles(frame, cv2.HOUGH_GRADIENT, dp, minDist, param1, param2, minRadius, maxRadius)

	circles = np.uint16(np.around(circles))
	for i in circles[0,:]:
		# draw the outer circle
		cv2.circle(frame,(i[0],i[1]),i[2],(0,255,0),2)
		# draw the center of the circle
		cv2.circle(frame,(i[0],i[1]),2,(0,0,255),3)

	return frame