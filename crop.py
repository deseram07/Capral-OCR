import cv2

def crop(image):

	(height,width) = image.shape
	spacing_width = width/15
	spacing_height = height/9
	h1 = (spacing_height * 5 + spacing_height * 4) / 2
	h0 = (spacing_height * 3 + spacing_height * 4) / 2
	w0 = spacing_width * 4
	w1 = spacing_width * 10
	croped = image[h0:h1, w0:w1]
	return croped #(croped image)
