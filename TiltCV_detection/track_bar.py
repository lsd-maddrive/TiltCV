import cv2
import numpy as np

def nothing(x):
    pass

def createTrackbar():
	cv2.namedWindow('image')

	cv2.createTrackbar('DownH1','image', 61, 255, nothing)
	cv2.createTrackbar('UpH1','image', 84, 255, nothing)

	cv2.createTrackbar('DownS','image', 55, 255, nothing)
	cv2.createTrackbar('UpS','image', 255, 255, nothing)

	cv2.createTrackbar('DownV','image', 8, 255, nothing)
	cv2.createTrackbar('UpV','image', 255, 255, nothing)

	cv2.createTrackbar('erosion','image', 4, 20, nothing)
	cv2.createTrackbar('dilation','image', 4, 20, nothing)

	cv2.createTrackbar('PWM_output_limit','image', 30, 100, nothing)
	cv2.createTrackbar('PWM_MF_change_value_1','image', 20, 100, nothing)

	cv2.createTrackbar('high_value_fuzzy','image', 200, 500, nothing)
	cv2.createTrackbar('medium_value_fuzzy','image', 110, 500, nothing)

	cv2.createTrackbar('deviation','image', 0, 240, nothing)

	cv2.createTrackbar('number of measurements','image', 0, 20, nothing)

def getFuzzy():
	PWM_output_limit = cv2.getTrackbarPos('PWM_output_limit','image')
	PWM_MF_change_value_1 = cv2.getTrackbarPos('PWM_MF_change_value_1','image')
	high_value_fuzzy = cv2.getTrackbarPos('high_value_fuzzy','image')
	medium_value_fuzzy = cv2.getTrackbarPos('medium_value_fuzzy','image')

	return PWM_output_limit, PWM_MF_change_value_1, high_value_fuzzy, medium_value_fuzzy


def getValueHSV():

	DownH1 = cv2.getTrackbarPos('DownH1','image')
	UpH1 = cv2.getTrackbarPos('UpH1','image')

	DownS = cv2.getTrackbarPos('DownS','image')
	UpS = cv2.getTrackbarPos('UpS','image')

	DownV = cv2.getTrackbarPos('DownV','image')
	UpV = cv2.getTrackbarPos('UpV','image')


	lower_value = np.array([DownH1,DownS,DownV])
	upper_value = np.array([UpH1,UpS,UpV])

	return lower_value, upper_value

def getValueMorphIter():

	erosion_iter = cv2.getTrackbarPos('erosion','image')
	dilation_iter = cv2.getTrackbarPos('dilation','image')

	return erosion_iter, dilation_iter


def getValueDeviation():

	center_deviation = cv2.getTrackbarPos('deviation','image')
	return center_deviation

def getValue_number_of_measurements():

	return cv2.getTrackbarPos('number of measurements','image')