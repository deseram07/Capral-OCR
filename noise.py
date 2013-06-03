import cv2
import numpy as np

def noise(image, img_shape, lower, higher):
	drawing = np.zeros(img_shape, np.uint8)
	
	ret,thresh = cv2.threshold(image, 0, 255, cv2.THRESH_OTSU)
	# thresh = cv2.adaptiveThreshold(imgray,240,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,89,1)


	contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	cv2.drawContours(drawing, contours, -1, (255,255,255), -1)

	# removing noise
	for cnt in contours:
		if cv2.contourArea(cnt) < int(lower) or cv2.contourArea(cnt) > int(higher):
			cv2.drawContours(drawing, [cnt], -1, (0,0,0), -1)

	return drawing