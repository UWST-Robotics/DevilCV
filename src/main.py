import cv2

import numpy as np

#cap = cv2.VideoCapture(0)
c = cv2.VideoCapture(0)

# show the camera feed

while True:
    ret, frame = c.read()
    if not ret:
        break
    cv2.imshow("Camera", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

c.release()