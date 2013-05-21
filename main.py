import detectwhitechar
import os.path

folder = 'E:\\2MP\\'
total = 0
match = 0
for f in os.listdir(folder):
	total += 1
	print f
	ext = [0,'']
	for i in f:
		if ext[0]:
			ext[1]+= i
		if i == '.':
			ext[0] = 1
	print ext
	if ext[1] == 'jpg' or ext[1] == 'JPG':
		match += detectwhitechar.detect(folder + f)
		# print match
		# print total

per = float(match)/float(total) * 100
print str(per) + "%"