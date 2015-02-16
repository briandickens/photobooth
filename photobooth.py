#####
#
# photobooth.py
# Brian Dickens
# 
# February 13, 2015
#
# 1. Take four photos
# 2. Replace background with underwater photo.
# 3. Write photos to onedrive.
# 4. Resize and arrange into 2x2
# 5. Add label to bottom.
# 6. Print photo.
#
#####

import time
import picamera
import io
from PIL import Image, ImageOps
import RPi.GPIO as GPIO

def takePhotosToFile(count):
    with picamera.PiCamera() as camera:
        camera.resolution = (1024, 768)
        for i in range(count):
            camera.capture('/home/pi/photobooth/pics/photobooth{}.jpg'.format(i+1))
            time.sleep(.5)

def takePhotosToPIL(count):
    images = []
    with picamera.PiCamera() as camera:
        camera.resolution = (1024, 768)
        # rotate the camera because when testing i had it upside down
        # (ribbon should come out the bottom)
        camera.rotation = 180 
        for i in range(count):
            stream = io.BytesIO()
            # Turn the LED on so i know it's taking a photo.
            camera.led = True
            camera.capture(stream, format = 'jpeg')
            # Turn the LED off so i know it's done taking a photo.
            camera.led = False
            stream.seek(0)
            images.append(Image.open(stream))
            time.sleep(2)
    return images

if __name__ == '__main__':
    
            
