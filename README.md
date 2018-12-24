# Neural-Network-Labelling-Generator

DEPENDENCIES: (get from Neural-Network-Labelling-Tool README.md links)

Python 2

PIL


Allows quick generation of datasets without individually labelling each image.

Will take images without the labelled object in it, modify the image by adding a given image of the object at a random coordinate and at a random size.  The corresponding text file is generated accordingly in a given file folder.

NOTE: This decreases images to label, but still must individually label images of the object at verying orientations.  Recommended to generate 100 images per one hand-labelled one.


INSTRUCTIONS:

Details are in the program.

Edit code, input file directories specific to computer/user.

Create an image of the to-label object with a clear background and ensure the size of the image matches to edges of the object in the image.
