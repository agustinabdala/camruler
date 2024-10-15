import cv2
import numpy as np
import utils
import math

camera_url = "rtsp://medicion:medicion2024@172.21.117.30:554/cam/realmonitor?channel=1&subtype=0"


cap = cv2.VideoCapture(camera_url)  # set video capture device``
cap.set(10, 160)  # set brightness
cap.set(3, 1280)  # set height and width for 720p camera
cap.set(4, 720)

scaleFactor = 1
widthPaper = 210 * scaleFactor
heightPaper = 297 * scaleFactor

calibrated = False


while True:
    success, img = cap.read()  # grabs, decodes and returns next video frame
    # resized = cv2.resize(img, (0, 0), None, 0.5, 0.5)
    # cv2.imshow('Original', resized)

    imgContours, conts = utils.getContours(
        img, showCanny=True, minArea=400, filter=4)

    # if len(conts) != 0:
    #     # pre-sorted so that first is largest, and find it's approx points
    #     biggestCont = conts[0][2]
    #     imgWarp = utils.warpImage(
    #         img, biggestCont, widthPaper, heightPaper)
    #     cv2.imshow('Letter Paper', imgWarp)

    imgContours2, conts2 = utils.getContours(
        img, minArea=400, filter=4, cThr=[50, 50], draw=False)

    if len(conts2) != 0:
        for obj in conts2:
            cv2.polylines(imgContours2, [obj[2]], True, (0, 255, 0), 2)
            nPoints = utils.reorder(obj[2])
            nW = round(utils.findDistance(
                nPoints[0][0]//scaleFactor, nPoints[1][0]//scaleFactor)/10, 2)
            nH = round(utils.findDistance(
                nPoints[0][0]//scaleFactor, nPoints[2][0]//scaleFactor)/10, 2)
            # display measurements on image
            cv2.arrowedLine(imgContours2, (nPoints[0][0][0], nPoints[0][0][1]), (nPoints[1][0][0], nPoints[1][0][1]),
                            (255, 0, 255), 2, 8, 0, 0.05)
            cv2.arrowedLine(imgContours2, (nPoints[0][0][0], nPoints[0][0][1]), (nPoints[2][0][0], nPoints[2][0][1]),
                            (255, 0, 255), 2, 8, 0, 0.05)
            x, y, w, h = obj[3]
            cv2.putText(imgContours2, '{}mm'.format(nW), (x + 30, y - 10), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                        (255, 0, 255), 1)
            cv2.putText(imgContours2, '{}mm'.format(nH), (x - 70, y + h // 2), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                        (255, 0, 255), 1)

            if (calibrated == False):
                scaleFactor, calibrated = utils.calibrate(scaleFactor, nW, nH, widthPaper, heightPaper, tol=0.01)
    
    cv2.imshow('cont2', imgContours2)
    cv2.waitKey(10)  # 400 ms delay, avoid kernel crash
