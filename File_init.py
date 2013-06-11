#initiates image capture in hand held device
#
#Author: Buddhika De Seram

from ftplib import FTP 
import datetime
import sys

mylist = []
today = datetime.date.today()
mylist.append(today)

ftp = FTP('10.204.12.89', 'pi', 'raspberry')
ftp.cwd('./sap/control')

# setting up init file
f = open('capture.txt', 'w')
f.write("__INIT__(CAPTURE)\n" + str(mylist[0]) + "\n")
f.close()

# transfering the file
ftp.storbinary('STOR CAPTURE.txt', open('./capture.txt', 'rb'))
print ftp.nlst()

ftp.close() 
