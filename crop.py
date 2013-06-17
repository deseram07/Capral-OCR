#Obtains required region of interest from input image
#
#Author: Buddhika De Seram
import cv2

def crop(image):

	(height,width) = image.shape
	spacing_width = width/15
	spacing_height = height/9
	h1 = (spacing_height * 7 + spacing_height * 6) / 2
	h0 = (spacing_height * 2 + spacing_height * 3) / 2
	# w0 = spacing_width * 4
	w0 = 0
	w1 = width
	croped = image[h0:h1, w0:w1]
	return croped #(croped image)
