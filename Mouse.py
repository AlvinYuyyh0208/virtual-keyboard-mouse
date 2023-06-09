import cv2
import numpy as np
import cvzone.HandTrackingModule as htm
import time
import autopy
from multiprocessing import Process, Array

# 在检测出手之前有卡顿的情况
cap = cv2.VideoCapture(0)

detector = htm.HandDetector(maxHands=1)
wCam, hCam = 1280, 720
frameR = 100  # frame reduction
cap.set(3, wCam)

cap.set(4, hCam)
pTime = 0

# size of screen
wScr, hScr = autopy.screen.size()
# print(wScr, hScr)

smoothening = 7

# previous location
plocX, plocY = 0, 0

# current location
clocX, clocY = 0, 0

def move_consumer(array: Array):
    while True:
        autopy.mouse.move(array[0], array[1])
        time.sleep(0.01)


def run():
    global plocX, plocY, clocX, clocY, pTime
    array = Array('f', [0, 0])
    p = Process(target=move_consumer, args=(array,))
    p.start()
    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)
        img = detector.findHands(img)
        lmList, bbox = detector.findPosition(img)

        if len(lmList) != 0:
            x1, y1 = lmList[8][0:]
            x2, y2 = lmList[12][0:]
            # print(x1, y1, x2, y2)

            # check finger up
            fingers = detector.fingersUp()
            # print(fingers)
            # 框架简化，可控制的范围
            cv2.rectangle(img, (frameR, frameR), (wCam - frameR,
                          hCam - frameR), (255, 0, 255), 2)
            if fingers[1] == 1 and fingers[2] == 0:
                # 鼠标的坐标
                x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
                y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))

                # 改变鼠标平滑度
                clocX = plocX + (x3 - plocX) / smoothening
                clocY = plocY + (y3 - plocY) / smoothening

                # autopy.mouse.move(clocX, clocY)
                array[0], array[1] = clocX, clocY
                cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)

                plocX, plocY = clocX, clocY

                # when click
            if fingers[1] == 1 and fingers[2] == 1:
                length, img, lineInfo = detector.findDistance(8, 12, img)
                print(length)
                # 左键单击
                if length < 30:
                    cv2.circle(
                        img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                    autopy.mouse.click()
                # 右键单击
                if length > 160:
                    autopy.mouse.click(autopy.mouse.Button.RIGHT)

        # fps
        cTime = time.time()

        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)), (20, 50),
                    cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
        img = detector.findHands(img)

        cv2.imshow("image", img)
        cv2.waitKey(1)

if __name__ == '__main__':
    run()