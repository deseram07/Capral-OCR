import cv2
import numpy as np
import pytesser
import cv2.cv as cv
import string
import sys
from dbfpy import dbf
from noise1 import *
import os
from crop import *
from check_valid import *
import time

RED_MIN = np.array((150,100,200))
RED_MAX = np.array((160,240,255))

def detect(filename, folder, file_no):
	# print 'in'
	img = cv2.imread(filename)
	img = cv2.medianBlur(img, 1) #smothing image

	# extracting white characters
	image1 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	imgray = crop(image1)



	imgray = cv2.resize(imgray, (800,150))
	(h,w) = imgray.shape
	(img_h,img_w) = (h,w)


	drawing = noise(imgray, imgray.shape, 1000, 25000)

	cv2.imshow('win1', drawing)
	cv2.waitKey()
	cv2.imwrite('E:\\Results\\res.jpg', drawing)

	# character recorgnition
	image = cv.LoadImage("E:\Results\\res.jpg", cv.CV_LOAD_IMAGE_GRAYSCALE)
	# cv2.imshow('image', image)
	# cv2.waitKey()
	cv.NamedWindow('image', cv.CV_WINDOW_AUTOSIZE)
	cv.ShowImage('image', image)
	cv.WaitKey()
	lang = ['eng']
	result = 0
	for i in lang:
		data = pytesser.iplimage_to_string(image, 'eng', pytesser.PSM_SINGLE_LINE,makebox=True)

	print data
	
	word = ''
	section = []	#all the characters and coordinates in a list
	line = []
	for i in data:
		if i == ' ' or  i=='\n':
			line.append(word)
			word = ''
		elif (i!='\n'):
			word+=i
		if i == '\n':
			section.append(line)
			line = []

	coord = []
	chars = []	#coordinates of the characters
	count = 0
	for i in section:
		for j in i:
			# print count
			if j.isdigit() and count < 5 and count > 0:
				coord.append(int(j))
			count += 1
		count = 0
		chars.append(coord)
		coord = []	

	# removing all symbols
	dele= 0
	delete=[]

	for i in section:
		if not i[0].isdigit() and not i[0].isalpha():
			delete.append(dele)
		dele += 1
	delete.reverse()
	for i in delete:
		section.pop(i)
		chars.pop(i)

	c = 0
	point = []
	for i in chars:
		cv2.rectangle(drawing,(i[0],i[1]),(i[2],i[3]),(255,255,255),2)

	counter = 0
	line_coordinates = [0]
	if len(chars) == 1:
		for i in chars:
			if i[0] > 400:
				line_coordinates.append(i[0]/2)
				line_coordinates.append(i[0])

	for i in chars:
		counter += 1
		if c == 0:
			point.append(i[2])
			c = 1
		elif c == 1:
			point.append(i[0])
			line = ((point[0] + point[1]) / 2)
			line_coordinates.append(line)
			cv2.line(drawing,(line,img_h),(line,0),(255,255,255),2)
			c = 0
			point = []
		if counter == len(chars):
			
			if img_w - i[2] > 50:
				line_coordinates.append(img_w)
			else:
				line_coordinates.append(i[2])
			cv2.line(drawing,(i[2],img_h),(i[2],0),(255,255,255),2)
	
	# spliting image and processing
	
	iterator = 1
	id = ''
	while iterator < len(line_coordinates):

		roi = imgray[0:img_h, line_coordinates[iterator-1]:line_coordinates[iterator]]
		iterator += 1
		corrected = noise(roi, roi.shape, 300, 10000)
		cv2.imwrite('E:\\report\\res.jpg', corrected)
		cv2.imshow('win1', corrected)
		cv2.waitKey()
		image = cv.LoadImage("E:\Results\\res.jpg", cv.CV_LOAD_IMAGE_GRAYSCALE)
		data = pytesser.iplimage_to_string(image, 'eng', 7 )
		print data
		for i in data:
			if i.isalpha() or i.isdigit():
				if i == 'O' or i =='o':
					i = '0'
				if i == 'L' or i == 'l':
					i = '1'
				if i == 'i' or i == 'I':
					i = '1'
				id = id + i

	print id
	sol = check(id)
	final = sol[0]
	alternative = sol[1]
	possible = sol[2]
	# print sol
	
	if not final:
		os.chdir(folder)
		filename = 'error' + str(file_no) 
		img_name = filename + '.jpg'
		txt_name = filename + '.txt'
		cv2.imwrite(img_name, img)
		
		if len(alternative) > 1:		#storing alternatives in a text file
			f = open(txt_name, 'w')
			for i in alternative:
				f.write(i+'\n')
			f.close()
		return None
	else:
		return possible
