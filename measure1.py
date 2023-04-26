import cv2
import numpy as np
import utils

cap = cv2.VideoCapture(2)  # set video capture device``
#cap.set(10, 10)  # set brightness
cap.set(3, 1280)  # set height and width for 720p camera
cap.set(4, 720)
pixel_cm_ratio = 1

# Load Aruco detector
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_50)
parameters = cv2.aruco.DetectorParameters()

 
while True:
    # success, img = cap.read()  # grabs, decodes and returns next video frame
    img = cv2.imread("media/IMG_1525.JPG")
    img = cv2.resize(img, (0, 0), None, 0.5, 0.5)
    # Get Aruco marker
    corners, _, _ = cv2.aruco.detectMarkers(
        img, aruco_dict, parameters=parameters)
    if corners:

        # Draw polygon around the marker
        int_corners = np.int0(corners)
        cv2.polylines(img, int_corners, True, (0, 255, 0), 1)

        # Aruco Perimeter
        aruco_perimeter = cv2.arcLength(corners[0], True)

        # Pixel to cm ratio
        pixel_cm_ratio = aruco_perimeter / (187*4)


    imgContours2, conts2 = utils.getContours(
        img, minArea=400, filter=4, cThr=[140, 197], draw=False, showCanny=True)

    if conts2:
        for obj in conts2:
            cv2.polylines(imgContours2, [obj[2]], True, (0, 255, 0), 2)
            nPoints = utils.reorder(obj[2])
            nW = round(utils.findDistance(
                nPoints[0][0]//pixel_cm_ratio, nPoints[1][0]//pixel_cm_ratio), 2)
            nH = round(utils.findDistance(
                nPoints[0][0]//pixel_cm_ratio, nPoints[2][0]//pixel_cm_ratio), 2)
            # display measurements on image
            cv2.arrowedLine(imgContours2, (nPoints[0][0][0], nPoints[0][0][1]), (nPoints[1][0][0], nPoints[1][0][1]),
                            (0, 0, 255), 2, 8, 0, 0.05)
            cv2.arrowedLine(imgContours2, (nPoints[0][0][0], nPoints[0][0][1]), (nPoints[2][0][0], nPoints[2][0][1]),
                            (0, 0, 255), 2, 8, 0, 0.05)
            x, y, w, h = obj[3]
            cv2.putText(imgContours2, '{}mm'.format(nW), (x + 30, y - 10), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                        (0, 0, 255), 1)
            cv2.putText(imgContours2, '{}mm'.format(nH), (x - 70, y + h // 2), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                        (0, 0, 255), 1)

    cv2.namedWindow("cont2", cv2.WINDOW_NORMAL) 
    cv2.imshow('cont2', imgContours2)
    cv2.waitKey(10)  # 400 ms delay, avoid kernel crash
