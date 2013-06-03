from dbfpy import dbf
import os

# def getdata():
os.chdir('E:\\database')
dbf1 = dbf.Dbf('E:\\database\\SEGMENT.dbf', new=False)
f = open('available.txt', 'w')
counter = 0
for rec in dbf1:
	if rec['P_QTY'] == 0:
		counter = 0
		for i in rec['P_CODE']:
			counter += 1
			if i.isalpha() or i.isdigit():
				f.write(i)
				# print i
			if len(rec['P_CODE']) == counter:
				f.write('\n')
f.close()
