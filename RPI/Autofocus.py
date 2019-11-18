import cv2 #sudo apt-get install python-opencv
import numpy as py
import os
import time
import subprocess
from subprocess import call

try:
	import picamera
	from picamera.array import PiRGBArray
except:
	sys.exit(0)
	
def focusing(val):
	value = (val << 4) & 0x3ff0
	data1 = (value >> 8) & 0x3f
	data2 = value & 0xf0
	os.system("i2cset -y 0 0x0c %d %d" % (data1,data2))
	
def sobel(img):
	img_gray = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY) #makes the image grayscale 
	img_sobel = cv2.Sobel(img_gray,cv2.CV_16U,1,1) #applies a sobel filter to the image - basically a filter that calculates gradient magnitudes
	return cv2.mean(img_sobel)[0] #larger gradient magnitudes indicate "sharper" edges 
	#taking the mean is probably for noise reduction 

def laplacian(img):
	img_gray = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
	img_sobel = cv2.Laplacian(img_gray,cv2.CV_16U)   
	return cv2.mean(img_sobel)[0]
	

def calculation(camera):
	#subprocess.call(["gcc","capture.c"])
	#rawBMP = subprocess.call() #"./a.out"
	#print('Getting BMP') 
	#convert BMP to RGB array 
	
	rawCapture = PiRGBArray(camera) #allows you to obtain a 3D numpy array (rows,columns,colors) from an unencoded RGB capture 
	print(rawCapture)	
	camera.capture(rawCapture,format="bgr", use_video_port=True) 
	image = rawCapture.array #sets the 
	print('This is the rawCapture array')
	print(image)
	rawCapture.truncate(0) #empties the rawCapture array
	print('This is the truncated rawCapture')
	print(rawCapture.truncate(0))
	return laplacian(image) 
	
	
if __name__ == "__main__":
	#call(["./capture"])
	call(["./arducamstill", "-t 10 -m 3 -awb 1 -ae 1 -f 65535"])
    #open camera
	#camera = picamera.PiCamera() #don't need this line anymore because arducamstill opens a camera instance 
	#open camera preview
	#camera.start_preview() becomes: 
	call(["./preview-camera0"]) #this isn't showing the pop-up screen for some reason  
	#set camera resolution to 640x480(Small resolution for faster speeds.)
	camera.resolution = (640, 480)

	print("Start focusing")
	
	max_index = 10
	max_value = 0.0
	last_value = 0.0
	dec_count = 0
	focal_distance = 10
	
	while True:
	    #Adjust focus
		focusing(focal_distance)
		#Take image and calculate image clarity
		val = calculation(camera)
		#Find the maximum image clarity
		if val > max_value:
			max_index = focal_distance
			max_value = val
			
		#If the image clarity starts to decrease
		if val < last_value:
			dec_count += 1
		else:
			dec_count = 0
		#Image clarity is reduced by six consecutive frames
		if dec_count > 6:
			break
		last_value = val
		
		#Increase the focal distance
		focal_distance += 10
		if focal_distance > 1000:
			break

    #Adjust focus to the best
	focusing(max_index)
	time.sleep(1)
	#set camera resolution to 2592x1944
	camera.resolution = (2592,1944)
	#save image to file.
	#camera.capture("test.jpg") becomes: 
	call(["./capture -f max_index"]) #is this going to be interpreted as an integer??? 	
	#call(["./capture -f 65535"]) #is this going to be interpreted as an integer??? 	
	print("max index = %d,max value = %lf" % (max_index,max_value))
	#while True:
	#	time.sleep(1)
		
	camera.stop_preview()
	camera.close()
		
	
