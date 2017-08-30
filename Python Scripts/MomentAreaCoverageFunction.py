# import the necessary packages
from imutils import paths
import argparse
import cv2
import numpy
import math
import random
import  os, os.path
from matplotlib import pyplot

from PIL import Image
from scipy import stats

def MomentAreaCoverage(imageName,imageCV2 ):

    sizeX = numpy.size(imageCV2,1)
    sizeY = numpy.size(imageCV2,0)

    # print "Image:"+imageName
    # print "sizeX:"+str(sizeX)
    # print "sizeY:"+str(sizeY)

    data = numpy.empty(256,dtype=int)
    histogram = numpy.empty(256,dtype=float)

    for i in range(256):
        data[i] = 0
        histogram[i] = 0

    total = 0.0
    m0 = 1.0
    m1 = 0.0
    m2 = 0.0
    m3 = 0.0

    threshold = -1

    #make a data out of this
    for x in range(sizeX):
        for y in range(sizeY):
            color = imageCV2[y,x][0] #get r of color since RGB should be same
            data[color] += 1

    for i in range(256):
        total += data[i]

    for i in range(256):
        histogram[i] = data[i]/total
        # print ""+str(i)+" , "+str(histogram[i])

    #Calculate first second third order moments
    for i in range(256):
        m1 += i*histogram[i]
        m2 += i*i*histogram[i]
        m3 += i*i*i*histogram[i]

    #first 4 moments of gray-level image equals first 4 moments of binary image
    #4 equalities with solution in Tsai's paper as follows

    cd = m0*m2 - m1*m1
    c0 = (-m2*m2 + m1*m3)/cd
    c1 = (m0*-m3 + m2*m1)/cd
    z0 = 0.5*(-c1-numpy.sqrt(c1*c1-4.0*c0))
    z1 = 0.5*(-c1+numpy.sqrt(c1*c1-4.0*c0))
    p0 = (z1-m1)/(z1-z0) #fraction of pixels that should be binary

    #find threshold from fraction
    sumHist = 0
    for i in range(256):
        sumHist+=histogram[i]
        if sumHist>p0:
            threshold = i
            break

    # print "threshold:"+str(threshold)
    # print "fraction:"+str(p0)


    #################################
    #show image with threshold
    #################################

    # cv2.imshow("ImageBefore: "+imageName, imageCV2)
    # for x in range(sizeX):
    #     for y in range(sizeY):
    #         if imageCV2[y, x][0] <= threshold:
    #             imageCV2[y, x] = [0, 0, 0]
    #         else:
    #             imageCV2[y, x] = [255, 255, 255]

    # cv2.imshow("ImageAfter: "+imageName, imageCV2)
    # key = cv2.waitKey(0)

    #################################
    #plot histogram
    #################################
    # pyplot.plot(range(256),histogram)
    # # pyplot.xlim(min(x)-1,max(x)+1)
    # # pyplot.ylim(min(y)-1,max(y)+1)
    #
    # #show threshold line
    # pyplot.plot([threshold,threshold], [0,max(histogram)])
    #
    # pyplot.xlabel('Brightness: 0-255')
    # pyplot.ylabel('Pixel Fraction')
    # pyplot.title("Color Histogram: "+str(imagePath))
    # pyplot.show()

    return threshold;