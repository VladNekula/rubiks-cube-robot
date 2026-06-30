import cv2
import numpy as np

def detect_color(h, s, v):

    if v < 50:
        return "B"

    if s < 50 and v > 150:
        return "W"

    if 0 <= h < 10 or h > 170:
        return "R"

    if 10 <= h < 25:
        return "O"

    if 25 <= h < 40:
        return "Y"

    if 40 <= h < 85:
        return "G"

    if 85 <= h < 140:
        return "B"

    return "?"

def scan_face(cam_index=0, face_name="U"):
    cap = cv2.VideoCapture(cam_index)
    print(f"[INFO] Покажите сторону {face_name}")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape
        size = 80

        start_x = w // 2 - size
        start_y = h // 2 - size

        colors = []

        for i in range(3):
            row = []
            for j in range(3):
                x = start_x + j * size
                y = start_y + i * size
                roi = frame[y:y+size, x:x+size]
                hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
                avg = hsv.mean(axis=(0, 1))
                color = detect_color(avg[0], avg[1], avg[2])
                row.append(color)
                cv2.rectangle(frame, (x, y), (x+size, y+size), (255, 255, 255), 2)
                cv2.putText(frame, color, (x+10, y+50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2)

            colors.append(row)

        cv2.putText(frame, f"FACE: {face_name}",
                    (30, 50), cv2.FONT_HERSHEY_SIMPLEX,
                    1.5, (0, 255, 0), 3)

        cv2.imshow("Scanner", frame)

        key = cv2.waitKey(1)

        if key == 32:
            cap.release()
            cv2.destroyAllWindows()
            return colors

        if key == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

    return None

def scan_cube():
    faces = ["U", "R", "F", "D", "L", "B"]
    cube = {}

    for i, face in enumerate(faces):
        result = scan_face(0, face)
        if result is None:
            print("Скан отменён")
            return None
        cube[face] = result
        print(f"[OK] {face} считан")
    return cube
