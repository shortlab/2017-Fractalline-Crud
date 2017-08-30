# import the necessary packages
from imutils import paths
import argparse
import cv2
import numpy
import math
import os, os.path
import random
from PIL import Image
from scipy import stats
from matplotlib import pyplot
from matplotlib.legend_handler import HandlerLine2D

from MomentAreaCoverageFunction import MomentAreaCoverage

# ap = argparse.ArgumentParser()
# ap.add_argument("-i", "--images", required=True,
# 	help="path to input directory of images")
# ap.add_argument("-t", "--threshold", type=float, default=125.0,
# 	help="focus measures that fall below this value will be considered 'blurry'")
# args = vars(ap.parse_args())

# Box Counting
cutSizeY = 120
cutSizeX = 450

valid_images = [".jpg",".gif",".png",".tga",".tif"]

fractalDimensionsAll = []
porosityListAll = []
cutPixelsAll = []

fractalDimensionsSecondBatch = []
porositListSecondBatch = []
cutPixelsSecondBatch =[]


fractalDimensionsAllShifted = []
firstFractalDimensionIntercept = -1

CRUD_folders = []
# CRUD_folders.append("CRUD_Thick5_cross/Processed_From_Usable")

CRUD_folders.append("CRUD_5_TopView/CRUD_5_Topview_1")
CRUD_folders.append("CRUD_5_TopView/CRUD_5_Topview_2_Tilted")
CRUD_folders.append("CRUD_5_TopView/CRUD_5_Topview_3")
CRUD_folders.append("CRUD_5_TopView/CRUD_5_Topview_thick4")

CRUD_folders.append("Westinghouse/For_Analysis")

useLayering = False;

for CRUD_folder in CRUD_folders:

    print "Folder:"+CRUD_folder


    # for imagePath in paths.list_images(args["images"]):
    for fileName in os.listdir(CRUD_folder):

        # print "filename:"+str(fileName)

        ext = os.path.splitext(fileName)[1]

        # print "ext:" + str(ext)

        if ext.lower() not in valid_images:
            continue

        imagePath = os.path.join(CRUD_folder,fileName)

        boxSizes = []
        if useLayering:
            boxSizes = [2,3,5,6,10,15, 30] # initial box size in pixel
        else:
            boxSizes = [2, 3, 4, 5, 6, 8, 10, 15, 16, 32]  # initial box size in pixel

        imageCV2 = cv2.imread(imagePath)

        sizeX = numpy.size(imageCV2,1)
        sizeY = numpy.size(imageCV2,0)

        print "Image:"+ imagePath
        # print "sizeX:"+str(sizeX)
        # print "sizeY:"+str(sizeY)
        # print "boxSize:"+str(boxSizes)

        imageNormal = Image.open(imagePath)
        pixelsFull = imageNormal.load()

        cutStarts = []
        cutEnds = []
        fractalDimensions = []
        porosityList = []

        thresholds = []

        #loop through cut up image until the top
        if useLayering:
            numberOfCuts = sizeY/cutSizeY
        else:
            numberOfCuts = 1

        # get beginning and ending X position to crop
        midPixelX = sizeX / 2
        beginX = int(midPixelX - cutSizeX / 2)
        endX = int(beginX + cutSizeX)

        # calculate threshold
        croppedX_image = imageCV2[:, int(beginX):int(endX)]
        threshold = MomentAreaCoverage(imagePath, croppedX_image)
        print "\n\n\nthreshold:" + str(threshold)

        for cutCount in range(numberOfCuts):

            beginY = int(cutCount*cutSizeY)
            endY = int((cutCount+1)*cutSizeY)

            # print "beginX:"+str(beginX)
            # print "endX:" + str(endX)
            # print "beginY:" + str(beginY)
            # print "endY:" + str(endY)

            if useLayering:
                pixels = imageCV2[int(beginY):int(endY),int(beginX):int(endX)]
            else:
                pixels = imageCV2[1:1280,:]

            pixels_sizeX = numpy.size(pixels, 1)
            pixels_sizeY = numpy.size(pixels, 0)

            # # calculate threshold
            threshold = MomentAreaCoverage(imagePath, pixels)
            print "threshold:" + str(threshold)

            # print(pixels_sizeX)
            # print(pixels_sizeY)

            gx = [] # x coordinates of graph points
            gy = [] # y coordinates of graph points

            # print "theColor[0]"+str(theColor[0])
            # print "theColor[1]"+str(theColor[1])
            # print "theColor[2]"+str(theColor[2])

            #shade pixel below threshold as pixel
            #Also get porosity
            blackPixelCount = 0
            for x in range(cutSizeX):
                for y in range(cutSizeY):
                    if pixels[y, x][0] <= threshold:
                        pixels[y, x] = [0,0,0]
                        blackPixelCount += 1

            porosity = float(blackPixelCount)/float(cutSizeX*cutSizeY)
            porosityList.append(porosity)

            # cv2.imshow("Image", pixels)
            # key = cv2.waitKey(0)

            for boxSize in boxSizes:
                numberOfBoxesX = int(cutSizeX / boxSize)
                numberOfBoxesY = int(cutSizeY / boxSize)
                boxCount = 0

                # print("boxSize:",boxSize,numberOfBoxesX,numberOfBoxesY,range(boxSize))
                for by in range(numberOfBoxesY):
                    for bx in range(numberOfBoxesX):
                        # if there are any pixels in the box then increase box count
                        foundPixel = False
                        for ky in range(boxSize):
                            for kx in range(boxSize):
                                # print("Checking:",bx, by,kx,ky,boxSize * bx + kx)
                                if pixels[boxSize * by + ky,boxSize * bx + kx][0] <= threshold:
                                    foundPixel = True
                                    boxCount += 1
                                    break
                            if foundPixel:
                                break
                # print "boxSize:"+str(boxSize)
                # print "boxCount"+str(boxCount)
                # print "boxSize:" + str(math.log(1.0 / boxSize))
                # print "boxCount" + str(math.log(boxCount))
                gx.append(math.log(1.0 / boxSize))
                gy.append(math.log(boxCount))

            slope, intercept,r_value,p_value,std_err = stats.linregress(gx,gy)

            cutStarts.append(beginY)
            cutEnds.append(endY)

            fractalDimensions.append(slope)

            #This is to make graph with red dot for westinghouse
            if CRUD_folder != "Westinghouse/For_Analysis":
                fractalDimensionsAll.append(slope)
                porosityListAll.append(porosity)
                cutPixelsAll.append(endY)
            else:
                fractalDimensionsSecondBatch.append(slope)
                porositListSecondBatch.append(porosity)
                cutPixelsSecondBatch.append(endY)

            #     print("Fractal Dimension:", slope)
            # print("r-squared:", r_value**2)
            # print("std_err:", std_err)

        # Make a shifted graph
        # set fractal dimension target to first in list
        if firstFractalDimensionIntercept == -1:
            firstFractalDimensionIntercept = fractalDimensions[0]


        shift = firstFractalDimensionIntercept - fractalDimensions[0]
        for i in range(len(fractalDimensions)):
            fractalDimensionsAllShifted.append(fractalDimensions[i] + shift)

        print ""
        print "___"

        print "Fractal Dimensions , Porosity:"
        for i in range(len(fractalDimensions)):
            print str(fractalDimensions[i])+ " , "+str(porosityList[i])

    #     #plot of fractal dimension and porosity
    #     pyplot.figure(1)
    #     pyplot.plot(cutStarts,fractalDimensions)
    #     pyplot.plot(cutStarts, porosityList)
    #     pyplot.xlabel('starting pixel')
    #     pyplot.ylabel('fractal dimension vs porosity')
    #     pyplot.title("fractalDimensions and porosity: "+str(imagePath))
    #     pyplot.show()
    #
    #     # fractal dimension vs porosity
    #     pyplot.figure(2)
    #     lines = pyplot.plot(porosityList,fractalDimensions,'bo')
    # #     pyplot.setp(lines, color = 'r',linewidth=2.0)
    #     pyplot.xlabel('porosity')
    #     pyplot.ylabel('fractal dimension')
    #     pyplot.title("fractalDimensions vs porosity: " + str(imagePath))
    #     pyplot.show()
    #
    #     # fractal dimension analysis
    #     slope, intercept, r_value, p_value, std_err = stats.linregress(porosityList, fractalDimensions)
    #     print "\nFd vs P slope:"+str(slope)
    #     print "\nFd vs P intercept:" + str(intercept)


#All  plot of fractal dimension and porosity
pyplot.figure(1)
pyplot.plot(cutPixelsAll,fractalDimensionsAll,'bo')
pyplot.xlabel('pixels')
pyplot.ylabel('fractal dimension')
pyplot.title("fractalDimensions vs pixel: ")

#All  plot of fractal dimension and porosity
pyplot.figure(2)
pyplot.plot(cutPixelsAll,porosityListAll,'bo')
pyplot.xlabel('pixels')
pyplot.ylabel('porosity')
pyplot.title("porosity vs pixel: ")

# #All  fractal dimension vs porosity
# pyplot.figure(3)
# lines = pyplot.plot(porosityListAll,fractalDimensionsAll,'bo')
# #     pyplot.setp(lines, color = 'r',linewidth=2.0)
# pyplot.xlabel('porosity')
# pyplot.ylabel('fractal dimension')
# pyplot.title("fractalDimensions vs porosity: ")

#All  fractal dimension vs porosity
pyplot.figure(3)
line1 = pyplot.plot(porosityListAll,fractalDimensionsAll,'bo')
line2 = pyplot.plot(porositListSecondBatch,fractalDimensionsSecondBatch,'ro')
#     pyplot.setp(lines, color = 'r',linewidth=2.0)
pyplot.legend([line1, line2],['MIT CRUD Loop','Westinghouse'])

pyplot.xlabel('porosity')
pyplot.ylabel('fractal dimension')
pyplot.title("fractalDimensions vs porosity: ")


#All  plot of fractal dimension and porosity
# pyplot.figure(4)
# pyplot.plot(cutPixelsAll,fractalDimensionsAllShifted,'bo')
# pyplot.xlabel('pixels')
# pyplot.ylabel('Adjusted fractal dimension')
# pyplot.title("fractalDimensions vs pixel: ")

pyplot.show()

