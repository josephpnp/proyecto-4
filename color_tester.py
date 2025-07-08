import cv2 as cv
import numpy as np

azulAlto = np.array([200, 255, 255], dtype=np.uint8)
azulBajo = np.array([20, 150, 100], dtype=np.uint8)
cap = cv.VideoCapture(0)
while True:
    ret, frame = cap.read()
    if not ret:
        break

    hsv = cv.cvtColor(frame, cv.COLOR_BGR2LAB)

    mask = cv.inRange(hsv, azulBajo, azulAlto)

    kernel = np.ones((5, 5), np.uint8)
    erored_mask = cv.erode(mask, kernel, iterations=1)
    dilated_mask = cv.dilate(erored_mask, kernel, iterations=1)
    mask = dilated_mask

    contours = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)[-2]
    #cv.drawContours(frame, contours, -1, (0, 255, 0), 3)

    for contour in contours:
        area = cv.contourArea(contour)
        if area > 500:
            M = cv.moments(contour)
            if M['m00'] != 0:
                cx = int(M['m10'] / M['m00'])
                cy = int(M['m01'] / M['m00'])
                cv.circle(frame, (cx, cy), 7, (0, 0, 255), 10)
                newcountor = cv.convexHull(contour)
                #cv.drawContours(frame, [newcountor], 0, (255, 0, 0), 5)


    cv.imshow('frame', frame)
    cv.imshow('mask', mask)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows