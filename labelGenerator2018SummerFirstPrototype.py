#THIS WILL: edit a set of png negatives from the collection folder by drawing a object on it in a random location and of a random size.  raw file is ONE file that is not truncated and has only one bounding box.<-that is the image to be pasted on the negatives.  txt files will be generated in the collection folder with already labelled coordinated based on the raw file coordinated.

#INSTRUCTIONS:
#raw files needs PLEASE BE ONLY ONE BOUNDING BOX AND NOT TRUNCATED
#collection files is a mass of negatives
#ALL PNG (transparency)

from __future__ import with_statement
import os, os.path
import sys
import glob
import random
from PIL import Image, ImageDraw, ImageFont

txtEnd = ".txt"
jpgEnd = ".png"

padding = 10
smallestPercent = 50
largestPercent = 100

#raw pic must be PNG, JPG does not support transparency
rawPicDirectory = "/Users/kaylee/Desktop/rawBox/00001.png" #pic folder w/ ONE label
rawFileDirectory = "/Users/kaylee/Desktop/rawFile/00001.txt" #file folder w/ ONE label

collectionPicDirectory = "/Users/kaylee/Desktop/pto/" #negative pic folder (to be positive)
collectionFileDirectory = "/Users/kaylee/Desktop/to/" #empty file folder

rawBox = Image.open(rawPicDirectory)
rawBox = rawBox.convert("RGBA")
#rawBox.show()

allPics = "*"+jpgEnd #won't allow you to do it on same line
for imgAddress in glob.glob(collectionPicDirectory+allPics):
    print("hi")
    img = Image.open(imgAddress)
    img = img.convert("RGBA")
    final = Image.new("RGBA", img.size)
    final.paste(img, (0,0), img)
    ratio = (int)(random.randint(smallestPercent, largestPercent))
    print("WIDTH OF CUBE IS (will turn into int later)"+str(rawBox.size[0]*ratio/100.0))
    rawBox = rawBox.resize((rawBox.size[0]*ratio/100, rawBox.size[1]*ratio/100))
    coords1 = random.randint(padding, img.size[0]-rawBox.size[0]-padding)
    coords2 = random.randint(padding, img.size[1]-rawBox.size[1]-padding)
    final.paste(rawBox, (coords1 , coords2), rawBox)
    img.close()
    final.save(imgAddress)
    
    #generating pre-labelled files
    temp = imgAddress.split("/")
    filename = temp[len(temp)-1].split(".")[0]
    openedFile = open(collectionFileDirectory+filename+txtEnd, "w+")
    print(openedFile)
    originalOpenedFile = open(rawFileDirectory, "r")
    print(originalOpenedFile)
    for line in originalOpenedFile:
        print("IN")
        print(line)
        data = line.split(" ")
        name = data[0]
        
        width = float(data[6]) - float(data[4])
        height = float(data[7]) - float(data[5])
        
        newwidth = width * ratio / 100
        newheight = height * ratio / 100
        (xmin, ymin) = (coords1, coords2)
        (xmax, ymax) = (coords1+newwidth, coords2+newheight)
        openedFile.write(name+" 0.0 0 0.0 "+str(xmin)+" "+str(ymin)+" "+str(xmax)+" "+str(ymax)+" 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 \n")
    
    openedFile.close()
    originalOpenedFile.close()

rawBox.close()

