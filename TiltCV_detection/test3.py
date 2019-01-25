import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while (1):
    _, frame = cap.read()

    new_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    equ = cv2.equalizeHist(new_frame)

    res = np.hstack((new_frame,equ))

    cv2.imshow('res', res)


    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()