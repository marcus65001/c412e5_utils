import cv2
import numpy as np

img=cv2.imread("1.png")
uimg=cv2.UMat(img)

img_h=cv2.cvtColor(uimg, cv2.COLOR_BGR2HSV)

tag_l=np.array([100,92,86])
tag_h=np.array([106,200,152])

mask=cv2.inRange(img_h,tag_l,tag_h)

contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

if len(contours) != 0:
    max_contour = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(max_contour)
    cv2.rectangle(img_h,(x-10,y-10), (x + w+10, y + h+10), (0, 255, 0), 2)
    cv2.imshow("cont",img_h)
    cv2.waitKey(0)
    crop=cv2.UMat(img_h,[y-10,y+h+10],[x-10,x+w+10])
    crop = cv2.cvtColor(crop, cv2.COLOR_HSV2BGR)
    cv2.imshow("crop",crop)
    cv2.waitKey(0)
    cv2.destroyAllWindows()