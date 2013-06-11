# Extracts images from handheld device from the lastest folder created in device
#
#Author: Buddhika De Seram
from ftplib import FTP 
import datetime
import sys
import os
import errno
import time

count = 0
folder = 0
image_name = 'cap'
ext = '.jpg'
mylist = []
today = datetime.date.today()
mylist.append(today)

ftp = FTP('10.204.12.89', 'pi', 'raspberry')
today = str(mylist[0])
print today

ftp.cwd('/home/pi/sap/data/') #folder where images are stored in device

files = ftp.nlst()
print files
today_files = []
for i in files:
	if i[:len(today)] == today:
		today_files.append(i)
if today_files == []:
	print "no files in folder"
	sys.exit(0)

# read latest file
today_files.sort()
today_files.sort(key=lambda tup: tup[-1])
current = today_files[-1]
print current

home_dir = "E:\\Results\\" + today + "No" + str(folder) #dir in main computer to save file

while True:
	try:
		os.mkdir(home_dir)
		break
	except OSError, e:
		if e.errno == errno.EEXIST:
			folder += 1
			home_dir = "E:\\Results\\" + today + "No" + str(folder)	
		else:
			sys.exit(1)
current_dir = '~/sap/data/' + current + '/'
ftp.cwd(current_dir)

#extracts all images in folder
os.chdir(home_dir)
if ftp.nlst() != []:
	for filename in ftp.nlst():
		cmd = 'RETR ' + filename
		image  = open(filename, 'wb')
		ftp.retrbinary(cmd, image.write)
		return filename

else:
	os.rmdir(home_dir)
	return None
