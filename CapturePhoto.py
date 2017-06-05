__author__ = "Andrew Vo"
import cv2
import time
import numpy
import os, sys
import PIL
from PIL import Image
from PIL import ImageOps

print type(cv2)
frames = 30
rows = 2
columns = 2
WIDTH = 800
HEIGHT = 800
trim_row = 15
trim_column = 15
wait_time = 3
WHITE = (255, 255, 255)
GREY_SCALE = (0, 1)
column_grayscale = GREY_SCALE

frame=Image.new('RGB', (WIDTH, HEIGHT), WHITE)
camera=cv2.VideoCapture(0)

def CaptureImage():
    result, image=camera.read()
    image=cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image=Image.fromarray(image)
    return image

def mainloop():
    print 'Get Ready to Take Photos!\n'
    for i in xrange(frames):
        temp = CaptureImage()

    fixedHeight = (HEIGHT - ((rows + 1) * trim_row)) / rows
    fixedWidth = (WIDTH - ((columns - 1) * trim_column)) / columns

    for row in xrange(rows):
        for i in xrange(wait_time):
            print '%s...' % (wait_time - i)
            time.sleep(1)
        print '\nTaking Picture!\n'
        time.sleep(1)

        image = CaptureImage()
        image = ImageOps.fit(image, (fixedWidth, fixedHeight), PIL.Image.LANCZOS)
        y = (row * fixedHeight) + ((row + 1) * trim_row)
        for column in xrange(columns):
            x = (column * fixedWidth) + (column * trim_column)
            if column_grayscale[column]:
                frame.paste(ImageOps.grayscale(image), (x, y))
            else:
                frame.paste(image, (x, y))
    filename = "HexagonImage.gif"
    photoImage = frame.save(filename)
    frame.show();

satisfied=False
while satisfied != True:
    mainloop()
    print "Are you satisfied with your photo?\n"
    response = raw_input('(y/n): ')
    response = response.lower()
    if response == 'y':
        satisfied = True
    else:
        print "Retaking Photos!\n"
        time.sleep(.5)