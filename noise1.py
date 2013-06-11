import cv2
import numpy as np

def noise(image, img_shape, lower, higher):
	drawing = np.zeros(img_shape, np.uint8)
	
	ret,thresh = cv2.threshold(image, 0, 255, cv2.THRESH_OTSU)

	# imgray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	# (r,c) = image.shape
	# adder = 0
	# count = 0
	# for i in range(r):
	# 	for j in range(c):
	# 		if image[i,j] > 120:
	# 			adder += image[i,j]
	# 			count += 1
	# avg = adder/count
	# print avg
	# ret,thresh = cv2.threshold(image, avg, 255, 0)

	contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	cv2.drawContours(drawing, contours, -1, (255,255,255), -1)

	# removing noise
	for cnt in contours:
		if cv2.contourArea(cnt) < int(lower) or cv2.contourArea(cnt) > int(higher):
			cv2.drawContours(drawing, [cnt], -1, (0,0,0), -1)

	return drawing