import sys
import cv2
import numpy
import os


slide_dir = sys.argv[1]

image_dir = sys.argv[2]

ma = -10000000000
name = ""
file = open("20171013_20171014_20171015.txt", "w+")
i = 0
print("started")

image_dict = {}
slide_dict = {}
image_arr = []
slide_arr = []

i = 0
for image_name in os.listdir(image_dir):
    im = cv2.imread(image_dir + image_name, 0)
    im = cv2.fastNlMeansDenoising(im, None, 10,  7, 21)
    im = cv2.adaptiveThreshold(im,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
    im = cv2.Canny(im,100,200)

    image_dict[i] = image_name
    image_arr.append(im)
    print(image_name, "preprocessing done")
    i += 1

i = 0
for slide_name in os.listdir(slide_dir):
    slide = cv2.imread(slide_dir + slide_name, 0)
    
    slide = cv2.fastNlMeansDenoising(slide, None, 10,  7, 21)
    slide = cv2.adaptiveThreshold(slide,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
    slide = cv2.Canny(slide,100,200)
    
    slide_dict[i] = slide_name
    slide_arr.append(slide)
    print(slide_name, "preprocessing done")
    i += 1

for i in range(len(image_arr)):
    im = image_arr[i]
    imstd = numpy.std(im)
    im = numpy.subtract(im, numpy.mean(im))
    ma = -10000000000
    for j in range(len(slide_arr)):
        slide = slide_arr[j]
        slstd = numpy.std(slide)
        slide = cv2.resize(slide, (len(im[0]), len(im)))
        slide = numpy.subtract(slide, numpy.mean(slide))

        temp = numpy.sum(numpy.multiply(im, slide))/(imstd*slstd)

        if temp > ma:
            ma = temp
            name = slide_dict[j]
        # print(j)
    print(i, image_dict[i], name)
    file.write(image_dict[i] + " " + name + "\n")