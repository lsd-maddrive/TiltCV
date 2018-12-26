import cv2
import numpy as np

def nothing(x):
    pass

# config = {
	
# 	cv2.CV_CAP_PROP_FRAME_COUNT: 10,
# }
cv2.namedWindow('image')

cv2.createTrackbar('Contrast','image', 0, 300, nothing)

cap = cv2.VideoCapture(0)	

result = cap.set(cv2.CAP_PROP_CONTRAST, 0)

print(result)
#for param, value in config.iteritmes():
#	cv2.VideoCapture.set(param, value)

while(1):
	
	Contrast = cv2.getTrackbarPos('Contrast','image')

	contrast1 = Contrast / 1000

	result = cap.set(cv2.CAP_PROP_CONTRAST, contrast1)

	_, frame = cap.read()

	cv2.imshow('image', frame)
	
	k = cv2.waitKey(5) & 0xFF
	
	if k == 27:
		break