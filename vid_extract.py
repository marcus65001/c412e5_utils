import cv2
import numpy as np

tag_l=np.array([80,63,86])
tag_h=np.array([130,255,255])

vid_capture = cv2.VideoCapture("v1.webm")

if (vid_capture.isOpened() == False):
    print("Error opening the video file")
else:
    fps = vid_capture.get(5)
    print('Frames per second : ', fps, 'FPS')

    frame_count = vid_capture.get(7)
    print('Frame count : ', frame_count)

fc=0

while (vid_capture.isOpened()):
    ret, frame = vid_capture.read()
    fc+=1
    if fc<8891:
        continue
    if ret == True:
        uimg = cv2.UMat(frame[50:-30,50:-500,:])
        cv2.imshow('Framew', uimg)

        img_h = cv2.cvtColor(uimg, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(img_h, tag_l, tag_h)

        contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if len(contours) != 0:
            try:
                max_contour = max(contours, key=cv2.contourArea)
                if cv2.contourArea(max_contour)>500*500:
                    continue
                x, y, w, h = cv2.boundingRect(max_contour)
                cv2.rectangle(img_h, (x + 10, y + 10), (x + w - 10, y + h - 10), (0, 255, 0), 2)
                crop = cv2.UMat(img_h, [y + 10, y + h - 10], [x + 10, x + w - 10])
                crop = cv2.cvtColor(crop, cv2.COLOR_HSV2BGR)
                if (w * h < 20000) or (not (0.5 < w / h < 2.0)):
                    continue
                cv2.imshow('Frame', crop)
                cv2.imwrite("img/cap_{}.png".format(fc),crop)
            except:
                pass

        key = cv2.waitKey(20)

        if key == ord('q'):
            break
    else:
        break



vid_capture.release()
cv2.destroyAllWindows()