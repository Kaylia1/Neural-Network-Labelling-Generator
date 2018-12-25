#PURPOSE: This software will edit a set of png images without a given object from a given collection folder
                  #by drawing an object on it in a random location and of a random size.  The object drawn is the
                  #image of the raw file, ONE file that is not truncated and contains only one bounding box in the
                  #corresponding text file.  The image drawn will be at a random coordinate and a random size.
                  #After the image is pasted, text files will be generated in the collection folder with a corresonding
                  #name to the image file edited and with already labelled coordinated.
                  #NOTE: This will only generate one bounding box per image per run.
                  #WARNING: This program changes the contents within the given directories.  Png images will be
                                     #permenantly edited.

#INSTRUCTIONS:
#all text files will generate in KITTI format
#raw text file should be in KITTI format
#edit file paths
#run program

#TODO: Raw file with multiple bounding boxes is currently untested.

from __future__ import with_statement
import os, os.path
import sys
import glob
import random
from PIL import Image, ImageDraw, ImageFont

txtEnd = ".txt"
imgEnd = ".png" #must be png to support transparent backgrounds for the raw picture file, jpg works in the program but is not as effective for neural network training.

#---------------Can Edit the Following to User Preference----------------
padding = 10 #distance of generated image to the edge of the picture
smallestPercent = 50 #smallest percentage size of generated image
largestPercent = 100 #largest percentage size of generated image

#---------------Edit the Following---------------
#raw pic must be PNG, JPG does not support transparency
rawPicDirectory = "/Users/kaylee/Desktop/rawBox/anImage.png" #pic folder with one label
rawFileDirectory = "/Users/kaylee/Desktop/rawFile/aText.txt" #file folder with one label

collectionPicDirectory = "/Users/kaylee/Desktop/pto/" #picture folder (to be edited, names within can be any)
collectionFileDirectory = "/Users/kaylee/Desktop/to/" #empty file folder (to generate files)
#------------------Stop Editing--------------------

rawBox = Image.open(rawPicDirectory)
rawBox = rawBox.convert("RGBA")
#rawBox.show()

allPics = "*"+imgEnd
for imgAddress in glob.glob(collectionPicDirectory+allPics): #open every png image, with any name, within directory in loop

    #----------------Editing PNG Images----------------
    #open image and modify format
    #variable img is the original image and variable final is the edited image
    print("New image opened.")
    img = Image.open(imgAddress)
    img = img.convert("RGBA")
    final = Image.new("RGBA", img.size)
    final.paste(img, (0,0), img)

    #calculate random size of the image to generate
    ratio = (int)(random.randint(smallestPercent, largestPercent))
    print("WIDTH OF CUBE IS (will turn into int later)"+str(rawBox.size[0]*ratio/100.0))
    rawBox = rawBox.resize((rawBox.size[0]*ratio/100, rawBox.size[1]*ratio/100))

    #calculate new coordinates of the image to generate
    coords1 = random.randint(padding, img.size[0]-rawBox.size[0]-padding) #x values
    coords2 = random.randint(padding, img.size[1]-rawBox.size[1]-padding) #y values

    #implement changes
    final.paste(rawBox, (coords1 , coords2), rawBox) #edits the image
    img.close()
    final.save(imgAddress) #save edited image
    
    #----------------Generating labeled text files----------------
    #write a new text file at given directory
    temp = imgAddress.split("/")
    filename = temp[len(temp)-1].split(".")[0] #get the image filename to match with the text file filename
    openedFile = open(collectionFileDirectory+filename+txtEnd, "w+")
    print(openedFile)
    
    #read raw text file bounding box coordinates
    originalOpenedFile = open(rawFileDirectory, "r") 
    print(originalOpenedFile)

    #In case there are multiple bounding boxes in the raw text file, read each line of the file
    for line in originalOpenedFile:
        
        #retrieve data
        print(line)
        data = line.split(" ") 
        name = data[0] #name of object being generated

        #calculate width and height of raw file bounding box
        width = float(data[6]) - float(data[4])
        height = float(data[7]) - float(data[5])

        #calculate new coordinates of generated bounding box
        #ratio, coords1 and coords2 are from the generated image
        newwidth = width * ratio / 100
        newheight = height * ratio / 100
        (xmin, ymin) = (coords1, coords2)
        (xmax, ymax) = (coords1+newwidth, coords2+newheight)

        #write the bounding box to the text file
        openedFile.write(name+" 0.0 0 0.0 "+str(xmin)+" "+str(ymin)+" "+str(xmax)+" "+str(ymax)+" 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 \n")

    #close files
    openedFile.close()
    originalOpenedFile.close()

rawBox.close()

