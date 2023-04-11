import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import numpy as np

cap = cv2.VideoCapture(0)
# width
cap.set(3, 1280)
# height
cap.set(4, 720)
ret, frame = cap.read()

imTable = cv2.imread("Resources/table.png")
imOver = cv2.imread("Resources/over.png")
imBall = cv2.imread("Resources/ball.png", cv2.IMREAD_UNCHANGED)
imBat1 = cv2.imread("Resources/bat1.png", cv2.IMREAD_UNCHANGED)
imBat2 = cv2.imread("Resources/bat2.png", cv2.IMREAD_UNCHANGED)

detector = HandDetector(detectionCon=0.8, maxHands=2)

# intVol
ballPos = [100, 100]
speedX = 10
speedY = 10

gameOver = False

score = [0, 0]


def run():
    while True:
        _, img = cap.read()
        img = cv2.flip(img, 1)

        hands, img = detector.findHands(img, flipType=False)
        # overlay background
        img = cv2.addWeighted(img, 0.2, imTable, 0.8, 0)

        if hands:
            for hand in hands:
                x, y, w, h = hand['bbox']
                h1, w1, _ = imBat1.shape
                # 使得bat不越界，通过大量坐标测试
                y = np.clip(y, 33, 490)
                xl = np.clip(x, 30, 615)
                xr = np.clip(x, 640, 1220)

                # 控制球拍运动
                if hand['type'] == "Left":
                    img = cvzone.overlayPNG(img, imBat1, (xl, y))
                    if xl < ballPos[0] < xl + w1 and y < ballPos[1] < y + h1:
                        speedX = -speedX
                        ballPos[0] += 30
                        score[0] += 1
                else:
                    img = cvzone.overlayPNG(img, imBat2, (xr, y))
                    # 需加上小球外接矩形的w，因为在右侧无法直接接触到球的外接矩形
                    if xr < ballPos[0] + imBall.shape[0] < xr + w1 and y < ballPos[1] < y + h1:
                        speedX = -speedX
                        ballPos[0] -= 30
                        score[1] += 1

        # game over
        if ballPos[0] < 30 or ballPos[0] > 1220:
            gameOver = True
            img = imOver
            cv2.putText(img, str(score[0]).zfill(
                2), (110, 275), cv2.FONT_HERSHEY_PLAIN, 3, (171, 137, 27), 5)
            cv2.putText(img, str(score[1]).zfill(
                2), (460, 275), cv2.FONT_HERSHEY_PLAIN, 3, (73, 73, 204), 5)

        # if the game not over
        else:
            # move the ball many tests
            if ballPos[1] >= 523 or ballPos[1] <= 30:
                speedY = -speedY

            ballPos[0] += speedX
            ballPos[1] += speedY

            # lay the ball
            img = cvzone.overlayPNG(img, imBall, ballPos)

            cv2.putText(img, str(score[0]), (300, 650),
                        cv2.FONT_HERSHEY_PLAIN, 5, (171, 137, 27), 5)
            cv2.putText(img, str(score[1]), (900, 650),
                        cv2.FONT_HERSHEY_PLAIN, 5, (73, 73, 204), 5)
        cv2.imshow("Ping Pong Game", img)
        key = cv2.waitKey(1)
        if key == ord("r"):
            ballPos = [100, 100]
            speedX = 10
            speedY = 10
            gameOver = False
            score = [0, 0]
            imOver = cv2.imread("Resources/over.png")
