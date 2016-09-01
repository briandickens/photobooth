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

HALF_WIDTH = 175
HALF_HEIGHT = 200

PHOTO_WIDTH = HALF_WIDTH * 2
PHOTO_HEIGHT = HALF_HEIGHT * 2

FOOTER_HEIGHT = 130
BORDER_WIDTH = 10
BG_COLOR = (255,255,255)

PAGE_WIDTH = 1400
PAGE_HEIGHT = 1800

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

def assemblePhotoSheet(images):
    footer = Image.open('/home/pi/photobooth/resources/footer.jpg')
    final_photo = Image.new('RGB', (((PHOTO_WIDTH * 2) + (BORDER_WIDTH * 3)), (PHOTO_HEIGHT * 2) + (BORDER_WIDTH * 3) + FOOTER_HEIGHT,), BG_COLOR)
    for i in range(len(images)):
        images[i] = ImageOps.fit(images[i], (PHOTO_WIDTH, PHOTO_HEIGHT), centering = (0.5, 0.5))
        #images[i] = images[i].rotate(270)
        images[i] = ImageOps.autocontrast(images[i], cutoff=0)

    final_photo.paste(images[0], (BORDER_WIDTH, BORDER_WIDTH))
    final_photo.paste(images[1], ((BORDER_WIDTH * 2 + PHOTO_WIDTH), BORDER_WIDTH))
    final_photo.paste(images[2], (BORDER_WIDTH, ((BORDER_WIDTH * 2) + PHOTO_HEIGHT)))
    final_photo.paste(images[3], ((BORDER_WIDTH * 2 + PHOTO_WIDTH), (BORDER_WIDTH * 2 + PHOTO_HEIGHT)))
    final_photo.paste(footer, (BORDER_WIDTH, ((BORDER_WIDTH * 3) + (PHOTO_HEIGHT * 2)))) 
    return images, final_photo


if __name__ == '__main__':
    pass
