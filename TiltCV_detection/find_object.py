import cv2
import image_processing as ip

def nothing(x):
    pass



def finding_a_circle_around_the_contour(frame):

	dilation = ip.processing_morphological_operators(frame)

	x = None
	y = None
	_, contours, hierarchy = cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

	cv2.drawContours(frame,contours,0,(0,0,255),2)
	
	if contours:

		cnt = contours[0]
		(x,y), radius = cv2.minEnclosingCircle(cnt)
		center = (int(x),int(y))
		radius = int(radius)

		cv2.circle(frame,center,radius,(0,255,0),2)

return frame