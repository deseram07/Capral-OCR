#Looks for contours in the image and tries to extract only the character
#
#Author: Buddhika De Seram
import cv2
import numpy as np

def noise(image, img_shape, lower, higher):
	drawing = np.zeros(img_shape, np.uint8) #creates binary image with pixel value of 0 (black)
	
	ret,thresh = cv2.threshold(image, 0, 255, cv2.THRESH_OTSU)
	#Preforms Otsu thresholding on image
	contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	cv2.drawContours(drawing, contours, -1, (255,255,255), -1)
	#draws contours in binary image
	# removing noise
	for cnt in contours:
		if cv2.contourArea(cnt) < int(lower) or cv2.contourArea(cnt) > int(higher):
			cv2.drawContours(drawing, [cnt], -1, (0,0,0), -1)
	#deletes contours from image if area not between lower and higher variables
	return drawing
