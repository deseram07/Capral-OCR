import cv2
import numpy as np
import pytesser
import cv2.cv as cv
import string
import sys
from dbfpy import dbf


RED_MIN = np.array((150,100,200))
RED_MAX = np.array((160,240,255))

def detect(filename):
	dbf1 = dbf.Dbf('E:\\database\\SEGMENT.dbf', new=False)

	img = cv2.imread(filename)
	img = cv2.medianBlur(img, 9) #smothing image

	
	# # looking for laser points
	# tar = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	# redres = cv2.inRange(tar, RED_MIN, RED_MAX)
	# redcon,h = cv2.findContours(redres, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

	drawing = np.zeros(img.shape, np.uint8)

	# x_cord = []
	# y_cord = []

	# for cnt in redcon:
	# 	if cv2.contourArea(cnt) > 50:
	# 		M = cv2.moments(cnt)
	# 		x, y = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
	# 		x_cord.append(x)
	# 		y_cord.append(y)
	# 		cv2.circle(drawing, (x,y), 5, 255, 8, 8)
	# 		cv2.drawContours(drawing, [cnt], 0, (255,255,255), 5)

	# drawing = cv2.resize(drawing, (800,600))
	# cv2.imshow('win1', drawing)
	# cv2.waitKey()

	# # cropping image
	# x_cord.sort()
	# y_cord.sort()
	# print x_cord
	# print y_cord
	# w = (x_cord[3] - x_cord[0])
	# h = (y_cord[3] - y_cord[0])
	# cropped = img[y_cord[0]:y_cord[0] + h, x_cord[0]: x_cord[0]+w]


	# extracting white characters
	imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	(r,c) = imgray.shape
	adder = 0
	count = 0
	# for i in range(r):
	# 	for j in range(c):
	# 		if imgray[i,j] > 120:
	# 			adder += imgray[i,j]
	# 			count += 1
	# avg = adder/count
	# print avg
	avg = 120
	ret,thresh = cv2.threshold(imgray, 0, 255, cv2.THRESH_OTSU)
	contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	cv2.drawContours(drawing, contours, -1, (255,255,255), -1)

	# removing noise
	for cnt in contours:
		if cv2.contourArea(cnt) < 900:
			cv2.drawContours(drawing, [cnt], -1, (0,0,0), -1)


	drawing = cv2.resize(drawing, (250,40))

	# save image
	cv2.imwrite('E:\Results\\res.jpg', drawing)

	# character recorgnition
	image = cv.LoadImage("E:\Results\\res.jpg", cv.CV_LOAD_IMAGE_GRAYSCALE)
	# cv.ShowImage('win', image)
	lang = ['enm']
	result = 0
	for i in lang:
		data = pytesser.iplimage_to_string(image, i, pytesser.PSM_SINGLE_WORD) 

	# text editing
		lan = i
		id = ""
		txt = ''
		check = 0
		after = 0
		count = 0
		digflag = False
		sybflag = False
		midsection = False
		for i in data:
			if i.isdigit() or i.isalpha() or i=='-' or i=='~' or i=='/':
				txt += i

		ln = len(txt)
		id = ['','','']	#id broken down into 3 sections, ['starting 2 characters (1 character if digit)','NUMBERS before prefix', 'prefix'] 

		temp = ''


		
		for i in txt:
			count += 1 	#syncs with len function
			temp += i
			if count == 1: #first character
				if i.isdigit():
					digflag = True
				id[0]+=i


			elif count == 2: #second character
				if digflag:
					midsection = True
				else:
					id[0]+=i
				digflag = False	#reset flag

			elif count == 3:
				midsection = True

			elif count == (ln-2) or count == (ln-1):
				if ((not i.isdigit()) and (not i.isalpha())) or count == (ln-1):
					print "1=" +i
					sybflag = True
					midsection = False
				else:
					print "2= " + i
					midsection = True

			if sybflag:
				if i == 'o' or i == 'O':
					i = str(0)
				if i == 'z' or i == 'Z':
					i = str(2)
				if i == 's' or i == 'S':
					i = str(5)
				if i == 'I' or i == 'i' or i == 'l':
					i = str(1)
				if i.isalpha() or i.isdigit():
					id[2]+=i

			if midsection:
				if i == 'o' or i == 'O':
					i = str(0)
				if i == 'z' or i == 'Z':
					i = str(2)
				if i == 's' or i == 'S':
					i = str(5)
				if i == 'I' or i == 'i' or i == 'l':
					i = str(1)

				
				if i.isdigit():
					id[1]+=i
		
		print id
		print temp
		# if id !='':
		# 	print lan + '=' + id
		# 	for rec in dbf1:
		# 		for i in rec['P_CODE']:
		# 			for char in i:
		# 				if char.isalpha() or char.isdigit():
		# 					data += char
		# 					# print data
		# 		if data == id:
		# 			print "Found Match"
		# 			result = 1
		# 			break
		# 		else:
		# 			data = ''
		# else:
		# 	print "**Failed**"
	# print id
	cv2.imshow('win2', drawing)
	cv2.waitKey()
	return result
	

