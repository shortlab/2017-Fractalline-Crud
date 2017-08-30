# import the necessary packages
from imutils import paths
import argparse
import cv2
import numpy
import math
import random
import  os, os.path
from matplotlib import pyplot
import time

from PIL import Image
from scipy import stats
from OtsuFunction import Otsu
from MomentAreaCoverageFunction import MomentAreaCoverage
from statisticsPun import meanPun
from statisticsPun import standardDevPun


CRUD_folders = []

# CRUD_folders.append("TiC")
# CRUD_folders.append("TiCSS")
# CRUD_folders.append("TiN")
# CRUD_folders.append("TiNSS")
# CRUD_folders.append("TiO2")
# CRUD_folders.append("ZrC")
# CRUD_folders.append("ZrNSS")

# CRUD_folders.append("TiO2SS")
# CRUD_folders.append("ZrO2")
# CRUD_folders.append("ZrO2SS")

CRUD_folders.append("ZrCSS")
CRUD_folders.append("ZrN")

valid_images = [".jpg",".gif",".png",".tga",".tif",".bmp"]


for CRUD_folder in CRUD_folders:

    print "Folder:"+CRUD_folder

    momentFractionList =[]
    otsuFractionList = []

    totalMomentFraction = 0;
    totalOtsuFraction = 0;
    imageCount = 0;

    # for imagePath in paths.list_images(args["images"]):
    for fileName in os.listdir(CRUD_folder):

        # print "filename:"+str(fileName)

        ext = os.path.splitext(fileName)[1]

        # print "ext:" + str(ext)

        if ext.lower() not in valid_images:
            continue

        imagePath = os.path.join(CRUD_folder,fileName)

        imageCV2 = cv2.imread(imagePath)
        sizeX = numpy.size(imageCV2,1)
        sizeY = numpy.size(imageCV2,0)

        # print "Image:"+ imagePath
        # print "sizeX:"+str(sizeX)
        # print "sizeY:"+str(sizeY)
        # print "boxSize:"+str(boxSizes)

        momentThreshold = MomentAreaCoverage(imagePath, imageCV2)
        # print "momentThreshold:"+str(momentThreshold)

        otsuThreshold = Otsu(imagePath, imageCV2)
        # print "otsuThreshold:"+str(otsuThreshold)

        #get ThresholdFraction
        otsuTotal = 0.0
        momentTotal = 0.0

        createImage = True

        otsuImage = numpy.zeros((sizeY,sizeX,3),numpy.uint8)
        otsuImage[:] = [0,0,0]
        momentImage = numpy.zeros((sizeY, sizeX, 3), numpy.uint8)
        momentImage[:] = [0, 0, 0]

        for x in range(sizeX):
            for y in range(sizeY):
                if imageCV2[y, x][0] > otsuThreshold:
                    otsuTotal += 1
                    otsuImage[y,x] = [255,255,255]
                if imageCV2[y, x][0] > momentThreshold:
                    momentTotal += 1
                    momentImage[y, x] = [255, 255, 255]

        #write image to file
        cv2.imwrite(CRUD_folder + "/Otsu-" + fileName + ".png", otsuImage)
        cv2.imwrite(CRUD_folder + "/Moment-" + fileName + ".png", otsuImage)

        otsuFraction = otsuTotal/(sizeX*sizeY)
        momentFraction = momentTotal / (sizeX * sizeY)

        #statistics
        otsuFractionList.append(otsuFraction)
        momentFractionList.append(momentFraction)

        totalMomentFraction += momentFraction
        totalOtsuFraction += otsuFraction
        imageCount += 1

        # print individual
        print "Moment:"+ str(momentFraction)+",Otsu:"+str(otsuFraction)

    # statistics
    otsuMean = meanPun(otsuFractionList)
    momentMean = meanPun(momentFractionList)
    otsuStandardDev = standardDevPun(otsuFractionList)
    momentStandardDev = standardDevPun(momentFractionList)

    #print summary
    print "" + CRUD_folder + ": Moment:"+ str(totalMomentFraction / imageCount)+",Otsu:"+str(totalOtsuFraction / imageCount)
    print "" + CRUD_folder + ": Moment:" + str(momentMean) + ",Otsu:" + str(otsuMean)
    print "" + CRUD_folder + ": MomentSD:" + str(otsuStandardDev) + ",OtsuSD:" + str(momentStandardDev)
    print "\n\n"