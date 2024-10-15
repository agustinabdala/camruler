import cv2
import numpy as np

def getContours(img, cThr=[100, 100], showCanny=False, minArea=1000, filter=0, blur_kernel_size=5, kernel_size=2, dilate_iter=3, erode_iter=2, draw=False):
    imgGrey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGrey, (blur_kernel_size, blur_kernel_size), 1)
    imgCanny = cv2.Canny(imgBlur, cThr[0], cThr[1])
    kernel = np.ones((kernel_size, kernel_size))
    imgDial = cv2.dilate(imgCanny, kernel, iterations=dilate_iter)
    imgThreshold = cv2.erode(imgDial, kernel, iterations=erode_iter)

    if showCanny:
        resized = cv2.resize(imgThreshold, (0, 0), None, 0.5, 0.5)
        cv2.namedWindow('Canny', cv2.WINDOW_NORMAL)
        cv2.imshow('Canny', resized)

    contours, _ = cv2.findContours(imgThreshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    finalContours = []

    for contour in contours:
        area = cv2.contourArea(contour)
        if area > minArea:
            perimeter = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
            bbox = cv2.boundingRect(approx)
            if filter > 0:
                if len(approx) == filter:
                    finalContours.append([len(approx), area, approx, bbox, contour])
            else:
                finalContours.append([len(approx), area, approx, bbox, contour])

    finalContours = sorted(finalContours, key=lambda x: x[1], reverse=True)

    if draw:
        for con in finalContours:
            cv2.drawContours(img, con[4], -1, (0, 0, 255), 3)

    return img, finalContours

def reorder(points):
    points = points.reshape((4, 2))
    newPoints = np.zeros_like(points)
    add = points.sum(axis=1)
    newPoints[0] = points[np.argmin(add)]
    newPoints[3] = points[np.argmax(add)]
    diff = np.diff(points, axis=1)
    newPoints[1] = points[np.argmin(diff)]
    newPoints[2] = points[np.argmax(diff)]
    return newPoints

def findDistance(pt1, pt2):
    return np.linalg.norm(pt2 - pt1)
