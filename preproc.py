import cv2
# import imutils
import numpy as np
from pathlib import Path

# cv2.namedWindow("TrackedBars")
# cv2.resizeWindow("TrackedBars", 640, 240)

def on_trackbar(val):
    t_min = cv2.getTrackbarPos("tmin", "TrackedBars")
    t_max = cv2.getTrackbarPos("tmax", "TrackedBars")
    th3 = cv2.adaptiveThreshold(uimg, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, \
                               cv2.THRESH_BINARY, 400, 0)
    contours, hierarchy = cv2.findContours(th3, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    contours=sorted(contours,key=cv2.contourArea)
    for ct in contours:
        global h,w,c
        if cv2.contourArea(ct)>(h*w)*0.8:
            continue
        u2 = cv2.UMat(uimg.get())
        rect=cv2.minAreaRect(ct)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        cv2.drawContours(u2, [box], 0, (0, 0, 255), 2)
        cv2.imshow("cont", u2)
        break
    cv2.imshow("mask",mask)



# 0-33
# cv2.createTrackbar("tmin", "TrackedBars", 0, 255, on_trackbar)
# cv2.createTrackbar("tmax", "TrackedBars", 0, 255, on_trackbar)
# on_trackbar(0)

def proc(path="path.png"):
    img=cv2.imread(path.as_posix())
    gh,gw,c=img.shape
    cx=gh//2
    cy=gw//2
    mask_cir = np.zeros_like(img)
    mask_cir = cv2.circle(mask_cir, (cx, cy), max(cx,cy), (255, 255, 255), -1)
    uimg=cv2.UMat(cv2.bitwise_and(img,mask_cir))
    uimg=cv2.cvtColor(uimg,cv2.COLOR_BGR2GRAY)
    cv2.imshow("cap",uimg)
    # mask=cv2.inRange(uimg,1,34)
    mask = cv2.adaptiveThreshold(uimg, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, \
                                   cv2.THRESH_BINARY, 401, 0)
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    contours=sorted(contours,key=cv2.contourArea,reverse=True)
    u2=None
    print(path)
    for ct in contours:
        print((gh*gw),cv2.contourArea(ct))
        # global h,w,c
        if cv2.contourArea(ct)>(gh*gw)*0.3:
            continue
        if cv2.contourArea(ct)<32*32:
            continue
        u2 = mask.get()
        u2=cv2.cvtColor(u2,cv2.COLOR_GRAY2BGR)
        # rect=cv2.minAreaRect(ct)
        # box = cv2.boxPoints(rect)
        # box = np.int0(box)
        # cv2.drawContours(u2, [box], 0, (0, 0, 255), 2)
        # x, y, w, h = cv2.boundingRect(ct)
        # a=max(0,y-10)
        # b=min(gh,y+h+10)
        # a = max(0, y - 10)
        # d=min(gw,x+w+10)
        # cv2.rectangle(u2, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # u2 = cv2.UMat(u2, [a,b], [c,d])
        cv2.drawContours(u2, [ct], 0, (0, 0, 255), 2)
        u2=cv2.medianBlur(u2,5)
        # cv2.imshow("cont", u2)
        break
    # cv2.imshow("mask",mask)
    if u2 is not None:
        cv2.imwrite((path.parent/"p_{}".format(path.name)).as_posix(),u2)

p=Path("ptest")
for i in p.iterdir():
    proc(i)
# proc(Path("c2.png"))
# cv2.waitKey(0)