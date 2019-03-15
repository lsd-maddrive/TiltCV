import cv2
import numpy as np
import track_bar as tb


def conversion(frame):
	
	blur = cv2.GaussianBlur(frame,(3,3),0)
	hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

	return hsv



def boundaries_hsv(frame):

	hsv = conversion(frame)

	lower_value, upper_value = tb.getValueHSV()
	hsv_with_boundaries = cv2.inRange(hsv, lower_value, upper_value)

	return hsv_with_boundaries


def processing_morphological_operators(frame):

	hsv_with_boundaries = boundaries_hsv(frame)

	kernel = np.ones((3,3), np.uint8)
	erosion_iter, dilation_iter = tb.getValueMorphIter()
	erosion = cv2.erode(hsv_with_boundaries, kernel, iterations = erosion_iter)
	dilation = cv2.dilate(erosion, kernel, iterations = dilation_iter)

	return dilation



def processed_frame(frame):

	processed = cv2.bitwise_and(frame,frame, mask = dilation)
