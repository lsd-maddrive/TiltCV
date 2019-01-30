import cv2
import numpy as np 

cap = cv2.VideoCapture(0)


while(1):
	_, frame = cap.read()
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	# ret, thresh = cv2.threshold(gray,127,255,cv2.THRESH_BINARY)


	clahe = cv2.createCLAHE(clipLimit=2, tileGridSize=(8,8)) 
	cl1 = clahe.apply(gray)	

	edged = cv2.Canny(cl1,30,250)

	contours = cv2.findContours(edged, 1, 2)

	cnt = contours[0]

	(x,y), radius = cv2.minEnclosingCircle(cnt)
	center = (int(x), int(y))
	radius = int(radius)
	cv2.circle(frame,center,radius,(0,255,0),2)

	cv2.imshow('gray', frame)
	cv2.imshow('edged', edged)

	# cv2.imshow('thresh', thresh)


	k = cv2.waitKey(5) & 0xFF
	if k == 27:
		break