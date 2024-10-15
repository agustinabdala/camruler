import cv2

camera_url = "rtsp://medicion:medicion2024@172.21.117.30:554/cam/realmonitor?channel=1&subtype=0"


cap = cv2.VideoCapture(camera_url)

num = 0

while cap.isOpened():

    succes, img = cap.read()

    k = cv2.waitKey(5)

    if k == 27:
        break
    elif k == ord('s'): # wait for 's' key to save and exit
        cv2.imwrite('images/img' + str(num) + '.png', img)
        print("image saved!")
        num += 1

    cv2.namedWindow('Img', cv2.WINDOW_NORMAL)
    cv2.imshow('Img',img)

# Release and destroy all windows before termination
cap.release()

cv2.destroyAllWindows()