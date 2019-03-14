import cv2
import numpy as np

def createTrackbar():
	cv2.namedWindow('image')

	cv2.createTrackbar('DownH1','image', 65, 255, nothing)
	cv2.createTrackbar('UpH1','image', 92, 255, nothing)

	cv2.createTrackbar('DownS','image', 55, 255, nothing)
	cv2.createTrackbar('UpS','image', 255, 255, nothing)

	cv2.createTrackbar('DownV','image', 8, 255, nothing)
	cv2.createTrackbar('UpV','image', 255, 255, nothing)

	cv2.createTrackbar('erosion','image', 4, 20, nothing)
	cv2.createTrackbar('dilation','image', 4, 20, nothing)

	cv2.createTrackbar('minrad','image', 3, 255, nothing)
	cv2.createTrackbar('maxrad','image', 700, 1000, nothing)

	cv2.createTrackbar('deviation','image', 180, 240, nothing)


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