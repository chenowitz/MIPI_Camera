import cv2 #sudo apt-get install python-opencv
import numpy as py
import os
import time
import subprocess
from subprocess import call
from skimage import color, io
import matlibplot.pyplot as plt

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
	
	#rawCapture = PiRGBArray(camera) #allows you to obtain a 3D numpy array (rows,columns,colors) from an unencoded RGB capture 
	#print(rawCapture)	
	#camera.capture(rawCapture,format="bgr", use_video_port=True) 
	#image = rawCapture.array #sets the 
	'''print('This is the rawCapture array')
	print(image)
	rawCapture.truncate(0) #empties the rawCapture array
	print('This is the truncated rawCapture')
	print(rawCapture.truncate(0))
	return laplacian(image)'''
	
image_path = './home/pi/Documents/ArduCAM/MIPI_Camera/RPI/mode3'
	
def load(image_path):
    out = io.imread(image_path)
    out = out.astype(np.float64)/255;
    return out

def display(img):
    plt.figure()
    plt.imshow(img)
    plt.axis('off')
    plt.show()
    
	
if __name__ == "__main__":
    
    call(["./capture", "-f 1000"])
    samplePicture = cv.imread('./home/pi/Documents/ArduCAM/MIPI_Camera/RPI')
    laplacian(samplePicture)
    
    
    
    