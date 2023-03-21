import cv2 as cv

cv.namedWindow("TrackedBars")
cv.resizeWindow("TrackedBars", 640, 240)

img = cv.imread("c2.png")
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

def on_trackbar(val):
    blk = cv.getTrackbarPos("tmin", "TrackedBars")
    c = cv.getTrackbarPos("tmax", "TrackedBars")
    # gau = cv.getTrackbarPos("gau", "TrackedBars")

    # blurred = cv.GaussianBlur(gray, (gau, gau), 0)
    #
    # edged = cv.Canny(blurred, t_min, t_max)
    th3 = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, \
                               cv.THRESH_BINARY, 2*blk+3, c)

    cv.imshow("e", th3)

cv.createTrackbar("tmin", "TrackedBars", 0, 255, on_trackbar)
cv.createTrackbar("tmax", "TrackedBars", 0, 255, on_trackbar)
# cv.createTrackbar("gau", "TrackedBars", 1, 20, on_trackbar)
on_trackbar(0)

cv.waitKey(0)