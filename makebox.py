import cv2
import numpy as np
import pytesser
import cv2.cv as cv
import string
import sys
from dbfpy import dbf
from noise import *

RED_MIN = np.array((150,100,200))
RED_MAX = np.array((160,240,255))

def detect(filename):

	img = cv2.imread(filename)
	img = cv2.medianBlur(img, 5) #smothing image

	# extracting white characters
	imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	# print imgray.shape
	(h,w) = imgray.shape
	(img_h,img_w) = (h,w)

	drawing = noise(imgray, img.shape, 500, 25000)
	cv2.imshow('win1', img)
	cv2.waitKey()
	
	cv2.imwrite('E:\Results\\res.jpg', drawing)

	# character recorgnition
	image = cv.LoadImage("E:\Results\\res.jpg", cv.CV_LOAD_IMAGE_GRAYSCALE)
	lang = ['enm']
	result = 0
	for i in lang:
		data = pytesser.iplimage_to_string(image, i, pytesser.PSM_SINGLE_LINE,makebox=True) 
		
	# obtaining coordinates of boxs
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

	# print section
	counter = 0
	line_coordinates = [0]
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
			line_coordinates.append(i[2])
			if img_w - i[2] > 400:
				line_coordinates.append(img_w)
			cv2.line(drawing,(i[2],img_h),(i[2],0),(255,255,255),2)

	cv2.imshow('win2', drawing)
	cv2.waitKey()

	# print line_coordinates
	# spliting image and processing

	iterator = 1
	id = ''
	while iterator < len(line_coordinates):

		roi = imgray[0:img_h, line_coordinates[iterator-1]:line_coordinates[iterator]]
		iterator += 1
		corrected = noise(roi, roi.shape, 1000, 25000)
		cv2.imwrite('E:\Results\\res.jpg', corrected)
		cv2.imshow('win2', corrected)
		cv2.waitKey()

		image = cv.LoadImage("E:\Results\\res.jpg", cv.CV_LOAD_IMAGE_GRAYSCALE)
		data = pytesser.iplimage_to_string(image, 'eng', 7 )
		# print data
		for i in data:
			if i.isalpha() or i.isdigit():
				if i == 'O' or i =='o':
					i = '0'
				id = id + i

	# sort data from database
	flag = 1
	while flag:
		if len(id) < 4:
			print "Unmatched"
			break
		possible = []
		no_matches = []
		f = open('E:\\database\\available.txt', 'r')

		data = f.readlines()
		for i in data:
			i = i.strip('\n')
			# first check: is length of item in database same as id detected
			if len(i) == len(id):
				possible.append(i)
			
		if len(possible) == 0:
			break
		# second check: check if detected in one go
		for i in possible:
			if id == i:
				print "Matched"
				# print i
				flag = 0
				break
		# third check: check every character select most matching item in sequence
		
		highest_match = 0
		for i in possible:
			match = 0
			x = 0
			for j in id:
				if i[x] == j:
					match+=1
				x+=1

			no_matches.append(match)
		position = 0
		pos = 0
		alternative = []
		for i in no_matches:
			if i > highest_match:
				highest_match = i
				pos = position
				alternative = []
			if i == highest_match:
				alternative.append(position)
			position += 1
		if len(id)>5:
			error = 3
		else:
			error = 2

		if len(alternative) != 1:
			pos = alternative[0]
			print alternative
		if no_matches[pos] > (len(id) - error):
			print "true"
			break
		else:
			# print no_matches[pos]
			# print error
			# print len(id)
			print "Unmatch"
			break


	# print possible
	print id + '\n'
	return result