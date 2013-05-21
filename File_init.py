from ftplib import FTP 
import datetime
import sys

mylist = []
today = datetime.date.today()
mylist.append(today)

ftp = FTP('130.102.86.16', 'pi', 'raspberry')
ftp.cwd('./sap/SAP/control')

# setting up init file
f = open('capture.txt', 'w')
f.write("__INIT__(CAPTURE)\n" + str(mylist[0]) + "\n")
f.close()

# transfering the file
ftp.storbinary('STOR CAPTURE.txt', open('./capture.txt', 'rb'))
print ftp.nlst()

ftp.close() 