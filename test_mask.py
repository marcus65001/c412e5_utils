import cv2
import numpy as np
from imutils import contours


ROAD_MASK = [(20, 60, 0), (50, 255, 255)]


img=cv2.imread("12.png")
crop=img[400:-180,:,:]
hsv = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv, ROAD_MASK[0], ROAD_MASK[1])
cv2.imshow("m",mask)
cv2.waitKey(0)
cnts, hierarchy = cv2.findContours(mask,
                                               cv2.RETR_EXTERNAL,
                                               cv2.CHAIN_APPROX_NONE)
s_con,_=contours.sort_contours(cnts, method="left-to-right")
for i in range(len(s_con)):
    x, y, w, h = cv2.boundingRect(s_con[i])
    cv2.rectangle(crop, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.putText(crop, "{}".format(i + 1), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 50, 10), 2)
cv2.imshow("m",crop)
cv2.waitKey(0)