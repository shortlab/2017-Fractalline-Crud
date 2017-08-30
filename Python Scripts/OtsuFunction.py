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

def Otsu(imageName,imageCV2 ):

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

    threshold = -1
    total = 0.0

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

    #initialize variables
    totalIntensity = 0.0
    totalPoints = 0.0

    totalIntensityLessThanK = 0.0
    totalPointsBelowThreshold = data[0]
    betweenClassVariance = 0.0
    maxBetweenClassVariance = 0.0
    threshold = 0

    #initialize total intensity and total points
    for k in range(256):
        totalIntensity += k*data[k]
        totalPoints += data[k]


    #get betweenClassVariance for each possible threshold
    #find out its max

    for k in range(256):
        totalIntensityLessThanK += k*data[k]
        totalPointsBelowThreshold += data[k]

        #get denominator of variance eqn
        denominator = totalPointsBelowThreshold*(totalPoints-totalPointsBelowThreshold)

        if denominator != 0:
            numerator = (totalPointsBelowThreshold/totalPoints)*totalIntensity - totalIntensityLessThanK
            betweenClassVariance = numerator*numerator/denominator
        else:
            betweenClassVariance = 0

        #test for highest variance
        if betweenClassVariance > maxBetweenClassVariance:
            maxBetweenClassVariance = betweenClassVariance
            threshold = k

    #################################
    #show image with threshold
    #################################

    # cv2.imshow("ImageBefore: "+imageName, imageCV2)
    #
    # for x in range(sizeX):
    #     for y in range(sizeY):
    #         if imageCV2[y, x][0] <= threshold:
    #             imageCV2[y, x] = [0, 0, 0]
    #         else:
    #             imageCV2[y, x] = [255, 255, 255]
    #
    #
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