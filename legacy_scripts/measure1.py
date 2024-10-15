import cv2
import numpy as np

# RTSP camera URL
camera_url = "rtsp://medicion:medicion2024@172.21.117.30:554/cam/realmonitor?channel=1&subtype=0"

def main():
    # Initialize video capture
    cap = cv2.VideoCapture(camera_url)

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame.")
            break

        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Apply Gaussian Blur
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # Edge detection
        edges = cv2.Canny(blurred, 50, 150)

        # Find contours
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            # Calculate area and filter small contours
            area = cv2.contourArea(contour)
            if area > 100:  # Minimum area threshold
                # Get bounding box
                x, y, w, h = cv2.boundingRect(contour)

                # Draw rectangle around detected object
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # Display width and height
                cv2.putText(frame, f"W: {w} H: {h}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Show the processed frame
        cv2.imshow("Detected Objects", frame)

        # Exit on 'q' key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
