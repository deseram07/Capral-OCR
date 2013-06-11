import os
from dbfpy import dbf

dbf1 = dbf.Dbf('E:\\database\\SEGMENT.dbf', new=False)
vertex_folder = 'E:\\Code\\Capral-OCR\\Vertex'
filename = 'E:\\Code\\Capral-OCR\\vertex_name.txt'

def send(correct_file):
	os.chdir(vertex_folder)
	# correct_file: text file with correct files
	name = open(filename, 'r')
	num = name.readline()
	num.strip('\n')
	name.close()
	counter = int(num) 
	id = correct_file.readlines()

	edited = ''
	for i in id:
		vertex_file = open(str(counter)+'.PUT', 'w')
		i = i.strip("\n")
		for rec in dbf1:
			x = rec['P_CODE']
			for k in x:
				if k.isalpha() or k.isdigit():
					edited += k

			if edited == i:

				vertex_file.write('\"' +rec['P_CODE'] + '\",1')
			edited = ''
		vertex_file.close()
		counter += 1

	num = open(filename, 'w')
	num.write(str(counter))
	num.close()
