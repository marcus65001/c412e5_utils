import cv2
import numpy as np
#
# img=cv2.imread("1.png")
# uimg=cv2.UMat(img)
#
# img_h=cv2.cvtColor(uimg, cv2.COLOR_BGR2HSV)

tag_l=np.array([80,63,86])
tag_h=np.array([130,255,255])
# 100,163,107

def crop_minAreaRect(img, rect):
    # rotate img
    angle = rect[2]
    rows,cols = img.shape[0], img.shape[1]
    M = cv2.getRotationMatrix2D((cols/2,rows/2),angle,1)
    img_rot = cv2.warpAffine(img,M,(cols,rows))

    # rotate bounding box
    rect0 = (rect[0], rect[1], 0.0)
    box = cv2.boxPoints(rect0)
    pts = np.int0(cv2.transform(np.array([box]), M))[0]
    pts[pts < 0] = 0

    # crop
    img_crop = img_rot[pts[1][1]:pts[0][1],
                       pts[1][0]:pts[2][0]]

    return img_crop


cv2.namedWindow("TrackedBars")
cv2.resizeWindow("TrackedBars", 640, 240)

img = cv2.imread("cap.png")
imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

def on_trackbar(val):
    global imgHSV
    hue_min = cv2.getTrackbarPos("Hue Min", "TrackedBars")
    hue_max = cv2.getTrackbarPos("Hue Max", "TrackedBars")
    sat_min = cv2.getTrackbarPos("Sat Min", "TrackedBars")
    sat_max = cv2.getTrackbarPos("Sat Max", "TrackedBars")
    val_min = cv2.getTrackbarPos("Val Min", "TrackedBars")
    val_max = cv2.getTrackbarPos("Val Max", "TrackedBars")

    lower = np.array([hue_min, sat_min, val_min])
    upper = np.array([hue_max, sat_max, val_max])

    imgMASK = cv2.inRange(imgHSV, lower, upper)
    # mask = cv2.inRange(img_h, tag_l, tag_h)

    contours, hierarchy = cv2.findContours(imgMASK, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) != 0:
        try:
            max_contour = max(contours, key=cv2.contourArea)
            # x, y, w, h = cv2.boundingRect(max_contour)
            rect = cv2.minAreaRect(max_contour)
            # cv2.rectangle(img_h, (x - 10, y - 10), (x + w + 10, y + h + 10), (0, 255, 0), 2)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            imgc=img.copy()
            cv2.drawContours(imgc, [box], 0, (0, 0, 255), 2)
            cv2.imshow("cont", imgc)
            # cv2.waitKey(0)
            # crop = cv2.UMat(img_h, [y - 10, y + h + 10], [x - 10, x + w + 10])
            crop=crop_minAreaRect(img,rect)
            # crop = cv2.cvtColor(crop, cv2.COLOR_HSV2BGR)
            cv2.imshow("crop", crop)
            # cv2.waitKey(0)
        except:
            pass

    # cv2.imshow("Output1", img)
    # cv2.imshow("Output2", imgHSV)
    cv2.imshow("Mask", imgMASK)


cv2.createTrackbar("Hue Min", "TrackedBars", 0, 179, on_trackbar)
cv2.createTrackbar("Hue Max", "TrackedBars", 179, 179, on_trackbar)
cv2.createTrackbar("Sat Min", "TrackedBars", 0, 255, on_trackbar)
cv2.createTrackbar("Sat Max", "TrackedBars", 255, 255, on_trackbar)
cv2.createTrackbar("Val Min", "TrackedBars", 0, 255, on_trackbar)
cv2.createTrackbar("Val Max", "TrackedBars", 255, 255, on_trackbar)



# Show some stuff
on_trackbar(0)
# Wait until user press some key
cv2.waitKey()
cv2.destroyAllWindows()