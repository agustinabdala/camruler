import json
import cv2
import numpy as np
import utils

# Function to save the current slider values to a JSON file
def save_presets(filename='presets.json'):
    presets = {
        'Canny Threshold 1': cv2.getTrackbarPos('Canny Threshold 1', 'Trackbars'),
        'Canny Threshold 2': cv2.getTrackbarPos('Canny Threshold 2', 'Trackbars'),
        'Brightness': cv2.getTrackbarPos('Brightness', 'Trackbars'),
        'Contrast': cv2.getTrackbarPos('Contrast', 'Trackbars'),
        'Blur Kernel Size': cv2.getTrackbarPos('Blur Kernel Size', 'Trackbars'),
        'Morph Kernel Size': cv2.getTrackbarPos('Morph Kernel Size', 'Trackbars'),
        'Dilate Iterations': cv2.getTrackbarPos('Dilate Iterations', 'Trackbars'),
        'Erode Iterations': cv2.getTrackbarPos('Erode Iterations', 'Trackbars')
    }
    with open(filename, 'w') as f:
        json.dump(presets, f)
    print(f"Presets saved to {filename}")

# Function to load slider values from a JSON file and set the sliders
def load_presets(filename='presets.json'):
    try:
        with open(filename, 'r') as f:
            presets = json.load(f)
        cv2.setTrackbarPos('Canny Threshold 1', 'Trackbars', presets['Canny Threshold 1'])
        cv2.setTrackbarPos('Canny Threshold 2', 'Trackbars', presets['Canny Threshold 2'])
        cv2.setTrackbarPos('Brightness', 'Trackbars', presets['Brightness'])
        cv2.setTrackbarPos('Contrast', 'Trackbars', presets['Contrast'])
        cv2.setTrackbarPos('Blur Kernel Size', 'Trackbars', presets['Blur Kernel Size'])
        cv2.setTrackbarPos('Morph Kernel Size', 'Trackbars', presets['Morph Kernel Size'])
        cv2.setTrackbarPos('Dilate Iterations', 'Trackbars', presets['Dilate Iterations'])
        cv2.setTrackbarPos('Erode Iterations', 'Trackbars', presets['Erode Iterations'])
        print(f"Presets loaded from {filename}")
    except FileNotFoundError:
        print(f"Preset file {filename} not found. Using default values.")

# Adjust other functions to call these when needed

def initialize_capture(device=0, width=1280, height=720):
    cap = cv2.VideoCapture(device)
    cap.set(3, width)
    cap.set(4, height)
    return cap

def load_aruco_detector():
    aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_50)
    parameters = cv2.aruco.DetectorParameters()
    return aruco_dict, parameters

def adjust_brightness_contrast(img, brightness=255, contrast=127):
    brightness = brightness - 255
    contrast = contrast - 127
    if contrast != 0:
        alpha = contrast / 127.0 + 1.0
        gamma = brightness - 128 * alpha
    else:
        alpha = 1.0
        gamma = brightness
    return cv2.addWeighted(img, alpha, img, 0, gamma)

def process_frame(img, aruco_dict, parameters, pixel_cm_ratio, cThr1, cThr2, brightness, contrast, blur_kernel_size, kernel_size, dilate_iter, erode_iter):
    img = adjust_brightness_contrast(img, brightness, contrast)
    corners, _, _ = cv2.aruco.detectMarkers(img, aruco_dict, parameters=parameters)
    
    if corners:
        int_corners = np.int0(corners)
        cv2.polylines(img, int_corners, True, (0, 255, 0), 1)
        aruco_perimeter = cv2.arcLength(corners[0], True)
        pixel_cm_ratio = aruco_perimeter / (187 * 4)
        print(f'pixel_cm_ratio = {pixel_cm_ratio}')

    imgContours2, conts2 = utils.getContours(
        img, cThr=[cThr1, cThr2], minArea=400, filter=4, showCanny=True, 
        blur_kernel_size=blur_kernel_size, kernel_size=kernel_size, 
        dilate_iter=dilate_iter, erode_iter=erode_iter, draw=False)

    if conts2:
        for obj in conts2:
            cv2.polylines(imgContours2, [obj[2]], True, (0, 255, 0), 2)
            nPoints = utils.reorder(obj[2])
            
            if nPoints.shape != (4, 2):
                print("Error: nPoints shape is not (4, 2)")
                continue
            
            nW = round(utils.findDistance(nPoints[0] / pixel_cm_ratio, nPoints[1] / pixel_cm_ratio), 2)
            nH = round(utils.findDistance(nPoints[0] / pixel_cm_ratio, nPoints[2] / pixel_cm_ratio), 2)

            cv2.arrowedLine(imgContours2, (nPoints[0][0], nPoints[0][1]), (nPoints[1][0], nPoints[1][1]),
                            (0, 0, 255), 2, 8, 0, 0.05)
            cv2.arrowedLine(imgContours2, (nPoints[0][0], nPoints[0][1]), (nPoints[2][0], nPoints[2][1]),
                            (0, 0, 255), 2, 8, 0, 0.05)
            x, y, w, h = obj[3]
            cv2.putText(imgContours2, f'{nW}mm', (x + 30, y - 10), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255), 1)
            cv2.putText(imgContours2, f'{nH}mm', (x - 70, y + h // 2), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255), 1)
    
    return imgContours2

def on_trackbar_change(val):
    pass

def create_trackbar_window():
    cv2.namedWindow('Trackbars', cv2.WINDOW_NORMAL)
    cv2.createTrackbar('Canny Threshold 1', 'Trackbars', 140, 255, on_trackbar_change)
    cv2.createTrackbar('Canny Threshold 2', 'Trackbars', 197, 255, on_trackbar_change)
    cv2.createTrackbar('Brightness', 'Trackbars', 255, 510, on_trackbar_change)
    cv2.createTrackbar('Contrast', 'Trackbars', 127, 254, on_trackbar_change)
    cv2.createTrackbar('Blur Kernel Size', 'Trackbars', 5, 50, on_trackbar_change)
    cv2.createTrackbar('Morph Kernel Size', 'Trackbars', 2, 10, on_trackbar_change)
    cv2.createTrackbar('Dilate Iterations', 'Trackbars', 3, 10, on_trackbar_change)
    cv2.createTrackbar('Erode Iterations', 'Trackbars', 2, 10, on_trackbar_change)

def main():
    cap = initialize_capture()
    aruco_dict, parameters = load_aruco_detector()
    pixel_cm_ratio = 1
    create_trackbar_window()
    load_presets()  # Load presets at the start

    while True:
        success, img = cap.read()
        if not success:
            print("Failed to capture image")
            break

        cThr1 = cv2.getTrackbarPos('Canny Threshold 1', 'Trackbars')
        cThr2 = cv2.getTrackbarPos('Canny Threshold 2', 'Trackbars')
        brightness = cv2.getTrackbarPos('Brightness', 'Trackbars')
        contrast = cv2.getTrackbarPos('Contrast', 'Trackbars')
        blur_kernel_size = cv2.getTrackbarPos('Blur Kernel Size', 'Trackbars') | 1  # Ensure odd number
        kernel_size = cv2.getTrackbarPos('Morph Kernel Size', 'Trackbars') | 1  # Ensure odd number
        dilate_iter = cv2.getTrackbarPos('Dilate Iterations', 'Trackbars')
        erode_iter = cv2.getTrackbarPos('Erode Iterations', 'Trackbars')

        imgContours2 = process_frame(img, aruco_dict, parameters, pixel_cm_ratio, cThr1, cThr2, brightness, contrast, blur_kernel_size, kernel_size, dilate_iter, erode_iter)
        cv2.namedWindow("cont2", cv2.WINDOW_NORMAL)
        cv2.imshow('cont2', imgContours2)

        key = cv2.waitKey(10)
        if key & 0xFF == ord('q'):
            break
        elif key & 0xFF == ord('s'):
            save_presets()  # Save presets when 's' is pressed

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
