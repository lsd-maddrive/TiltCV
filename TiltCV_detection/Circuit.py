import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while(1):

	_, frame = cap.read()

	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	gray = cv2.GaussianBlur(gray, (3,3),0)

	clahe = cv2.createCLAHE(clipLimit=2, tileGridSize=(8,8)) 
	cl1 = clahe.apply(gray)	

	edged = cv2.Canny(cl1,30,250)

	kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
	closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)
	
	cnts = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[1]

	total = 0

	for c in cnts:

		peri = cv2.arcLength(c,True)

		approx = cv2.approxPolyDP(c,0.02 * peri, True)


		if len(approx) == 4:

			cv2.drawContours(frame,[approx], -1, (0,255,0),4)
			total += 1

	cv2.imshow('gray', gray)
	cv2.imshow('edged', edged)
	cv2.imshow('closed', closed)
	cv2.imshow('frame', frame)

	k = cv2.waitKey(5) & 0xFF
	
	if k == 27:
		break
