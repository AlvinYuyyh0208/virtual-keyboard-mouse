import cv2
import numpy as np

from cvzone.HandTrackingModule import HandDetector
from time import sleep
from pynput.keyboard import Controller, Key
import mediapipe as mp

from threading import Thread
from queue import Queue
import random
import time
import util

size = 1
q = Queue(size)

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(detectionCon=0.8)


keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "<--"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";", "UP"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/", "DOWN"]]
finalText = ""
Keyboard = Controller()


# 绘制键盘
# 此处顺序为BGR
def drawAll(img, buttonList):
    for button in buttonList:
        x, y = button.pos

        w, h = button.size
        cv2.rectangle(img, button.pos, (x + w, y + h),
                      (255, 0, 0), cv2.FILLED)  # start, size, color
        cv2.putText(img, button.text, (x + 20, y + 65),
                    cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)  # text, location, font, proportion, color, thickness

    return img


class Button():
    def __init__(self, pos, text, size):
        self.pos = pos
        self.text = text
        self.size = size


buttonList = []
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        if key == '<--':
            buttonList.append(
                Button([100 * j + 50, 100 * i + 50], key, (85 * 2, 85)))
        if key == 'UP':
            buttonList.append(
                Button([100 * j + 50, 100 * i + 50], key, (85 * 2, 85)))

        if key == 'DOWN':
            buttonList.append(
                Button([100 * j + 50, 100 * i + 50], key, (85 * 3, 85)))

        buttonList.append(Button([100 * j + 50, 100 * i + 50], key, (85, 85)))


def run():

    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)
        img = detector.findHands(img)
        lmList, bboxInfo = detector.findPosition(img)

        drawAll(img, buttonList)

        # 判断手指是否在按钮上
        if lmList:
            for button in buttonList:
                x, y = button.pos
                w, h = button.size
                # 8号为右手食指指尖
                if x < lmList[8][0] < x + w and y < lmList[8][1] < y + h:
                    cv2.rectangle(img, button.pos, (x + w, y + h),
                                  (160, 160, 160), cv2.FILLED)  # start, size, color
                    cv2.putText(img, button.text, (x + 20, y + 65),
                                cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255),
                                4)  # text, location, font, proportion, color, thickness

                    # 食指指尖和中指指尖的距离
                    l, _, _ = detector.findDistance(8, 12, img, draw=False)
                    print(l)

                    # 当点击的时候
                    if l < 30:
                        # start, size, color
                        cv2.rectangle(img, button.pos, (x + w, y + h),
                                      (255, 178, 102), cv2.FILLED)
                        cv2.putText(img, button.text, (x + 20, y + 65),
                                    cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255),
                                    4)
                        if button.text == '<--':
                            Keyboard.press(Key.backspace)
                            finalText = finalText[:-1]

                        if button.text == 'UP':
                            # 当前音量
                            util.increaseVolume()

                        if button.text == 'DOWN':
                            util.decreaseVolume()

                        else:
                            finalText += button.text
                            Keyboard.press(button.text)
                # 可更改
                sleep(0.15)

        # 绘制文本框
        cv2.rectangle(img, (50, 350), (700, 450), (160, 160, 160),
                      cv2.FILLED)  # start, size, color
        cv2.putText(img, finalText, (60, 425),
                    cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)

        cv2.imshow("image", img)
        cv2.waitKey(1)
