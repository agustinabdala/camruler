import numpy as np
import cv2 as cv
import glob
import pickle

# Load the camera calibration data from pickle files
with open("cameraMatrix.pkl", "rb") as f:
    cameraMatrix = pickle.load(f)

with open("dist.pkl", "rb") as f:
    dist = pickle.load(f)

# Read the image to be undistorted
img = cv.imread('img47.png')
h, w = img.shape[:2]

# Get the optimal new camera matrix and region of interest
newCameraMatrix, roi = cv.getOptimalNewCameraMatrix(cameraMatrix, dist, (w, h), 1, (w, h))

# Undistort the image
dst = cv.undistort(img, cameraMatrix, dist, None, newCameraMatrix)

# Crop the image
x, y, w, h = roi
dst = dst[y:y+h, x:x+w]

# Save the undistorted image
cv.imwrite('caliResult1.png', dst)

# Undistort with Remapping
mapx, mapy = cv.initUndistortRectifyMap(cameraMatrix, dist, None, newCameraMatrix, (w, h), 5)
dst = cv.remap(img, mapx, mapy, cv.INTER_LINEAR)

# Crop the image
dst = dst[y:y+h, x:x+w]
cv.imwrite('caliResult2.png', dst)

print("Undistortion complete. Results saved as 'caliResult1.png' and 'caliResult2.png'.")
