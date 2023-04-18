import cv2
import numpy as np
import math


def getContours(img, cThr=[100, 100], showCanny=False, minArea=1000, filter=0, draw=False):
    imgGrey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # convert into greyscale
    imgBlur = cv2.GaussianBlur(imgGrey, (5, 5), 1)
    imgCanny = cv2.Canny(imgBlur, cThr[0], cThr[1])
    kernel = np.ones((5, 5))
    imgDial = cv2.dilate(imgCanny, kernel, iterations=3)
    imgThreshold = cv2.erode(imgDial, kernel, iterations=2)
    if showCanny:
        resized = cv2.resize(imgThreshold, (0, 0), None, 0.6, 0.6)
        cv2.imshow('Canny', resized)

    contours, hierarchy = cv2.findContours(
        imgThreshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    finalContours = []

    for i in contours:
        area = cv2.contourArea(i)
        if area > minArea:
            perimeter = cv2.arcLength(i, True)
            approx = cv2.approxPolyDP(i, 0.02*perimeter, True)
            bbox = cv2.boundingRect(approx)
            if filter > 0:
                if len(approx) == filter:
                    finalContours.append([len(approx), area, approx, bbox, i])
            else:
                finalContours.append([len(approx), area, approx, bbox, i])

    # sort contour area from largest to smallest
    finalContours = sorted(finalContours, key=lambda x: x[1], reverse=True)

    if draw:
        for con in finalContours:
            cv2.drawContours(img, con[4], -1, (0, 0, 255), 3)

    return img, finalContours


def reorder(points):
    newPoints = np.zeros_like(points)
    points = points.reshape((4, 2))
    add = points.sum(1)
    newPoints[0] = points[np.argmin(add)]
    newPoints[3] = points[np.argmax(add)]
    diff = np.diff(points, axis=1)
    newPoints[1] = points[np.argmin(diff)]
    newPoints[2] = points[np.argmax(diff)]
    return newPoints


# gets a bird's-eye perspective of the image
def warpImage(img, points, w, h, pad=20):

    points = reorder(points)
    pts1 = np.float32(points)
    pts2 = np.float32([[0, 0], [w, 0], [0, h], [w, h]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    imgWarp = cv2.warpPerspective(img, matrix, (w, h))
    imgWarp = imgWarp[pad:imgWarp.shape[0]-pad, pad:imgWarp.shape[1]-pad]

    return imgWarp


def findDistance(pts1, pts2):
    return ((pts2[0] - pts1[0])**2 + (pts2[1] - pts1[1])**2)**0.5


def calibrate(scale_factor, nW, nH, widthPaper, heightPaper, tol=None, calibration_status_update=False, scale_tolerance = 0.01):
    r_orig = widthPaper / heightPaper
    r_calib = nW / nH
    new_scale_factor = scale_factor
    tol = 0.01 if tol == None else tol
    
    try:
        if (math.isclose(r_calib, r_orig, rel_tol=tol) and
            nH != 0 and heightPaper != 0 and calibration_status_update == False):
            
            new_scale_h = nH / heightPaper
            new_scale_w = nW / widthPaper
            
            if (math.isclose(new_scale_h, new_scale_w, rel_tol=scale_tolerance)):
                new_scale_factor = new_scale_h
                calibration_status_update = True

            print(nW, nH, f"scalefactor: {new_scale_factor} calib_status {calibration_status_update}")

        else:
            calibration_status_update = False


    except ZeroDivisionError:
        print('Cannot devide by zero.')
    print(f'WIDTH: {nW} HEIGHT: {nH}')
    return new_scale_factor, calibration_status_update