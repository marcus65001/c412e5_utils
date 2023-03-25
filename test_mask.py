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
s_con,_=contours.sort_contours(cnts, method="right-to-left")
cand=None
H,W,_=img.shape
for i in range(len(s_con)):
    if cv2.contourArea(s_con[i])<20:
        continue
    M = cv2.moments(s_con[i])
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
    print(cX, W // 2)
    if cX>W//2:
        cand=s_con[i]
    x, y, w, h = cv2.boundingRect(s_con[i])
    cv2.rectangle(crop, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.putText(crop, "{}".format(i + 1), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 50, 10), 2)
x, y, w, h = cv2.boundingRect(cand)
cv2.putText(crop, "{}".format("cand!"), (x+10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 50, 10), 2)
cv2.imshow("m",crop)
cv2.waitKey(0)