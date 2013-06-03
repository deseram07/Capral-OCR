from ftplib import FTP 
import datetime
import sys

ftp = FTP('10.204.12.89', 'pi', 'raspberry')
ftp.cwd('./sap/control')

# setting up init file
f = open('endcapture.txt', 'w')
f.write("__COMPLETE__(CAPTURE)")
f.close()


ftp.storbinary('STOR ENDCAPTURE.txt', open('./endcapture.txt', 'rb'))
print ftp.nlst()

ftp.close()