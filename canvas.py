import cv2
import numpy as np
import mediapipe as mp
from collections import deque

# Setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.75)
mp_draw = mp.solutions.drawing_utils

colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255), (255, 255, 255)]
color_names = ["BLUE", "GREEN", "RED", "YELLOW", "ERASER"]
colorIndex = 0

# Stroke data
strokes = []
points = [deque(maxlen=1024)]
index = 0

trail_points = deque(maxlen=10)
paintWindow = np.ones((480, 640, 3), dtype=np.uint8) * 255

def draw_buttons(frame):
    cv2.rectangle(frame, (20, 1), (120, 65), (0, 0, 0), 2)
    cv2.putText(frame, "CLEAR", (30, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)

    for i, (color, name) in enumerate(zip(colors, color_names)):
        x1, x2 = 130 + i * 100, 210 + i * 100
        cv2.rectangle(frame, (x1, 1), (x2, 65), color, -1)
        if colorIndex == i:
            cv2.rectangle(frame, (x1, 1), (x2, 65), (0, 0, 0), 2)
        text_color = (0, 0, 0) if name == "ERASER" else (255, 255, 255)
        cv2.putText(frame, name, (x1 + 5, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.5, text_color, 1)

def fingers_up(lms):
    fingers = []
    fingers.append(lms[4].x < lms[3].x)  # Thumb
    fingers += [lms[t].y < lms[t - 2].y for t in [8, 12, 16, 20]]
    return fingers

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    draw_buttons(frame)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        handLms = result.multi_hand_landmarks[0]
        lms = handLms.landmark
        mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)

        ix, iy = int(lms[8].x * 640), int(lms[8].y * 480)
        fingers = fingers_up(lms)

        if iy <= 65:
            if 20 <= ix <= 120:
                strokes.clear()
                paintWindow[67:, :, :] = 255
            for i in range(len(colors)):
                x1, x2 = 130 + i * 100, 210 + i * 100
                if x1 <= ix <= x2:
                    colorIndex = i
        else:
            if fingers[1] and not any(fingers[2:]):  # Only index finger up
                points[index].appendleft((ix, iy))
            elif all(fingers):  # All fingers up → New stroke
                strokes.append((list(points[index]), colors[colorIndex]))
                points.append(deque(maxlen=1024))
                index += 1
                trail_points.clear()
    else:
        points.append(deque(maxlen=1024))
        index += 1
        trail_points.clear()

    # Draw current strokes
    for stroke, color in strokes:
        for j in range(1, len(stroke)):
            if stroke[j - 1] and stroke[j]:
                cv2.line(frame, stroke[j - 1], stroke[j], color, 4)
                cv2.line(paintWindow, stroke[j - 1], stroke[j], color, 4)

    # Draw current live points
    for j in range(1, len(points[index])):
        if points[index][j - 1] and points[index][j]:
            cv2.line(frame, points[index][j - 1], points[index][j], colors[colorIndex], 4)
            cv2.line(paintWindow, points[index][j - 1], points[index][j], colors[colorIndex], 4)

    cv2.imshow("Air Canvas", frame)
    cv2.imshow("Paint", paintWindow)

    if cv2.waitKey(1) & 0xFF == 27:
        break

# Save the final drawing
cv2.imwrite("drawing.png", paintWindow)

cap.release()
cv2.destroyAllWindows()







