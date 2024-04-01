import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from PIL import Image, ImageFilter

#Load the image and set size of image
input_filename = "input.jpg"
output_filename = "output.jpg"
Image.MAX_IMAGE_PIXELS = None

img = Image.open(input_filename)
img.load()
img = img.resize((int(img.width * 0.5), int(img.height * 0.5)))

#Find edges of objects within the image (tissue/ fluid border), blur the image to remove noise
#Suggested blurring range (5, 13); (8,10) produces results with some noise but accurate shape
img = img.filter(ImageFilter.FIND_EDGES)
img = img.filter(ImageFilter.GaussianBlur(8))

#Build an array of pixel values to find the second mode, this will be the most occuring tissue pixel
#note: the first mode will be 0, the color of the image border
image_array = np.array(img)
height, width = image_array.shape
image_array = image_array.reshape(height * width, 1)

image_array = image_array[image_array != 0]
mode = sp.stats.mode(image_array)
threshold = mode.mode
print(threshold)

#If the pixel value is sufficiently close to the threshold value, categorize it as tissue (0)
#Else, categorize it as fluid (255)
img = img.point(lambda pixel: 0 if abs(pixel - threshold) > 4 else 255)

#Show the image using matplotlib
plt.imshow(img, cmap='Greys_r',  interpolation='nearest')
plt.show()