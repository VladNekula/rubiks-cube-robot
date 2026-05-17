import cv2
import numpy as np

def detect_color(h, s, v):

    if v < 50:
        return "B"

    if s < 40 and v > 150:
        return "W"

    if 20 < h < 35:
        return "Y"

    if 35 < h < 50:
        return "G"

    if 75 < h < 140:
        return "B"

    if h < 10 or h > 170:
        return "R"

    if 10 <= h <= 20:
        return "O"

    return "?"

def scan_face():

    cap = cv2.VideoCapture(0)

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        #frame = cv2.flip(frame, 1)

        h, w, _ = frame.shape

        size = 60

        start_x = w // 2 - size * 3 // 2
        start_y = h // 2 - size * 3 // 2

        colors = []

        for i in range(3):
            row = []

            for j in range(3):

                x = start_x + j * size
                y = start_y + i * size

                cv2.rectangle(     #рисует квадрат
                    frame,
                    (x, y),
                    (x + size, y + size),
                    (255, 255, 255),
                    2
                )

                roi = frame[y:y+size, x:x+size]    #1 квадратик

                hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

                avg = hsv.mean(axis=0).mean(axis=0)   #как я понял, берет средний цвет квадрата

                color = detect_color(avg[0], avg[1], avg[2])

                row.append(color)

                cv2.putText(
                    frame,
                    color,
                    (x + 20, y + 35),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (255, 255, 255),
                    2
                )

            colors.append(row) #собирает 3 на 3 матрицу

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
