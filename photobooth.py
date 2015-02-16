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
from PIL import Image

def takePhotosToFile(count):
    with picamera.PiCamera() as camera:
        camera.resolution = (1024, 768)
        for i in range(count):
            camera.capture('/home/pi/photobooth/pics/photobooth{}.jpg'.format(i+1))
            time.sleep(.5)
        
