import os
import cv2
import subprocess

def rename(foldername):
	os.chdir(foldername)

	for f in os.listdir(foldername):
		print f
		filename = foldername + f
		print filename
		filename = raw_input("Correct ID: ")
		os.rename(f, filename)
