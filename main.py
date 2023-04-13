

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox
from multiprocessing import Process


class Main(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 创建三个按钮并添加到窗口
        btn1 = QPushButton('键盘控制', self)
        btn1.move(0, 50)
        btn1.clicked.connect(self.keyboardClick)

        btn2 = QPushButton('鼠标控制', self)
        btn2.move(0, 100)
        btn2.clicked.connect(self.mouseClick)

        btn3 = QPushButton('小游戏', self)
        btn3.move(0, 150)
        btn3.clicked.connect(self.gameClick)

        # 设置窗口大小和标题
        self.setGeometry(300, 300, 200, 200)
        self.setWindowTitle('手势识别')
        self.show()

    def keyboardClick(self):
        import keyboard
        p = Process(target=keyboard.run)
        p.start()

    def mouseClick(self):
        import mouse
        p = Process(target=mouse.run)
        p.start()

    def gameClick(self):
        import game
        p = Process(target=game.run)
        p.start()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    sys.exit(app.exec_())
