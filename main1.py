import report
import os, errno
import random
from send_vertex import *
from getdata import *

folder = 'E:\\Thesis\\'
failed_name = 'fail'
h = '\\'
failed_folder = folder + failed_name + h
total = 0
match = open(folder+'match.txt', 'w')
print "Extrating data from database"
# getdata()

while True:
    try:
        os.mkdir(failed_folder)
        break
    except OSError, e:
        if e.errno == errno.EEXIST:
            #file already exists

            failed_folder = folder + failed_name + str(random.randint(0,200))+h

        else:
        #     #unknown error
            sys.exit(1)
for f in os.listdir(folder):
	total += 1

	ext = [0,'']
	for i in f:
		if ext[0]:
			ext[1]+= i
		if i == '.':
			ext[0] = 1

	if ext[1] == 'jpg' or ext[1] == 'JPG':
		id = report.detect(folder + f, failed_folder, total)
		# print "id = " + id
		if id != None:
			match.write(id + '\n')
			print "MATCHED " + id

match.close()
match = open(folder+'match.txt', 'r')
send(match)
match.close()

#check p quantity fie2drawing = np.zeros((h,w_t), np.uint8)print section

#renaming will be done in folder