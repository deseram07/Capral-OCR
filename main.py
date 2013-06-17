#This program calls the main recognition program. Before doing so
#the program makes the required folders to save the failes images
#and the text file to save the correct images
#
#Author: Buddhika De Seram

import makebox
import os, errno
import random
from send_vertex import *
from getdata import *

folder = 'E:\\afterthesis\\' #folder where images are stored, this should not change because the images 
						#will be processed as the main terminal receives them
failed_name = 'fail'	#folder name to store failed images
h = '\\'
failed_folder = folder + failed_name + h
total = 0
match = open(folder+'match.txt', 'w')	#text file name to store matched ID
print "Extrating data from database"

# getdata() #runs through database and extracts die ID's that are outside the vertex library

print "Extraction complete	"
#Creates new folder
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

#checks whether files is an image
	ext = [0,'']
	for i in f:
		if ext[0]:
			ext[1]+= i
		if i == '.':
			ext[0] = 1

	if ext[1] == 'jpg' or ext[1] == 'JPG':
		id = makebox.detect(folder + f, failed_folder, total)
		# print "id = " + id
		if id != None:
			match.write(id + '\n')	#writes matched die ID into text file
			print "MATCHED " + id

match.close()
match = open(folder+'match.txt', 'r')
send(match)
match.close()

