import cv2
import numpy as np

points = []

def mouse_callback(event, x, y, flags, param):
    global points, frame_hsv

    if event == cv2.EVENT_LBUTTONDOWN:

        hsv = frame_hsv[y, x]

        points.append(hsv)

        print("\nДобавлена точка:")
        print("HSV:", hsv)

        if len(points) >= 5:

            pts = np.array(points)

            h_min = int(np.min(pts[:, 0]))
            h_max = int(np.max(pts[:, 0]))

            s_min = int(np.min(pts[:, 1]))
            s_max = int(np.max(pts[:, 1]))

            v_min = int(np.min(pts[:, 2]))
            v_max = int(np.max(pts[:, 2]))

            print(f"H: {h_min} - {h_max}")
            print(f"S: {s_min} - {s_max}")
            print(f"V: {v_min} - {v_max}")

cap = cv2.VideoCapture(0)

cv2.namedWindow("frame")
cv2.setMouseCallback("frame", mouse_callback)

frame_hsv = None

print("Кликай по одному цвету (5 точек на один цвет)")

while True:

    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)

    frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    cv2.imshow("frame", frame)

    key = cv2.waitKey(1)

    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
