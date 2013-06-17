#Extracts the ID's of dies which are out of the vertex library
#from database file and saves in a text file
#
#Author: Buddhika De Seram

from dbfpy import dbf
import os

# hardcode the location of database file in computer
os.chdir('E:\\Code\\Capral-OCR\\database')	#switches to the location of the database file in the computer

#hardcode the database file including the location 
dbf1 = dbf.Dbf('E:\\Code\\Capral-OCR\\database\\SEGMENT.dbf', new=False)	#loading database file
f = open('available.txt', 'w')
counter = 0
for rec in dbf1:
	if rec['P_QTY'] == 0:
		counter = 0
		for i in rec['P_CODE']:
			counter += 1
			if i.isalpha() or i.isdigit():
				f.write(i)
			if len(rec['P_CODE']) == counter:
				f.write('\n')
f.close()
