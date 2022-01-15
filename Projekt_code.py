# -*- coding: utf-8 -*-
"""
Created on Sat Jan 15 08:45:55 2022

@author: isaak
"""

from picamera import PiCamera
import time
import RPi.GPIO as GPIO
import picamera.array
import numpy as np
from numpy import array as nparray
from numpy import sum as npsum



def checkRightSteering(right_pixels, white_pixel_value):
    for i in range(right_pixels.shape[0]):
        if (right_pixels[i] > white_pixel_value):
            return i
    return -1

def checkLeftSteering(left_pixels, white_pixel_value):
    i = left_pixels.shape[0] - 1
    while i > 0:
        if (left_pixels[i] > white_pixel_value):
            return left_pixels.shape[0] - i
        i = i - 1
    return -1



n = 1000
for i in range(n):
    with picamera.PiCamera() as camera:
        camera.resolution = (1920,1056)
        with picamera.array.PiRGBArray(camera) as output:
            camera.capture(output, 'rgb')
        

            bild = nparray(output.array)
            
            bild = npsum(bild,2)
            
            first_left_pixel = 1060

            first_right_pixel = 630

            pixel_read_height = 138

            array_length = 300

            white_val = 3*0.6

            steering_strength = 45

            left_array = bild[(first_left_pixel - array_length):first_left_pixel, pixel_read_height]
            right_array = bild[first_right_pixel:first_right_pixel + array_length, pixel_read_height]

            right = checkLeftSteering(right_array, white_val)
            left = checkLeftSteering(left_array, white_val)

            #angle = 90

            print(1)

            if right > 0:
                angle = 90 + (steering_strength*right/300)
            elif left > 0:
                angle = 90 - (steering_strength*left/300)
            else:
                angle = 90

            #set GPIO numbering mode
            GPIO.setmode(GPIO.BOARD)

            GPIO.setup(11,GPIO.OUT)
            servo1=GPIO.PWM(11,50)
            #11=pin, 50=50Hz pulse

            #start PWM running, but with value of = (pulse off)
            servo1.start(0)
            try:
                angle=float(angle)
                servo1.ChangeDutyCycle(2+(angle/18))
                time.sleep(0.01)
                servo1.ChangeDutyCycle(0)
                
            finally:
                servo1.stop()
                GPIO.cleanup()
