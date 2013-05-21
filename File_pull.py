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

ftp = FTP('130.102.86.16', 'pi', 'raspberry')
today = str(mylist[0])
print today

ftp.cwd('/home/pi/sap/SAP/data/')

files = ftp.nlst()
print files
today_files = []
for i in files:
	if i[:len(today)] == today:
		today_files.append(i)
if today_files == []:
	print "no files in folder"
	sys.exit(0)
today_files.sort()
current = today_files[-1]
print current

home_dir = "E:\\Results\\" + today + "No" + str(folder)

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
current_dir = '~/sap/SAP/data/' + current + '/'
ftp.cwd(current_dir)

os.chdir(home_dir)
if ftp.nlst() != []:
	for filename in ftp.nlst():
		cmd = 'RETR ' + filename
		image  = open(filename, 'wb')
		ftp.retrbinary(cmd, image.write)
		print filename
else:
	print "No files"
	# os.removedirs(home_dir)