import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QMenu, QDesktopWidget
from PyQt5.QtGui import QContextMenuEvent
from PyQt5.QtCore import Qt, QTimer, QPoint
import random

class DesktopPet(QMainWindow):
    def __init__(self, screenSize):
        super().__init__()
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)

        self.screenWidth = screenSize.width()
        self.screenHeight = screenSize.height()
        # self.setGeometry(screenSize.width() - 150,
        #                 screenSize.height() - 200,
        #                 150, 150)
        self.setGeometry(800,500,150,150)
        # self.posX = 800
        # self.posY = 500

        # self.setFixedSize(150, 150)
        # self.setGeometry(, self.pos, 150, 150)
        # self.center()
        self.oldPos = self.pos()
        # print(self.pos().x())
        self.posX = self.pos().x()
        self.posY = self.pos().y()

        self.char = QLabel(self)
        
        self.initUI()
        
        
    def initUI(self):
        self.char.setGeometry(0,0,150,150)
        self.char.setStyleSheet("border-image: url(./saka.png);")
        self.char.setCursor(Qt.PointingHandCursor)
        
        self.randomMoveTimer = QTimer(self)
        self.randomMoveTimer.timeout.connect(self.randomMove)
        self.randomMoveTimer.start(5000)

    def randomMove(self):
        possible_moves = ['right', 'left', 'up', 'down', 'stand']
        move = random.choice(possible_moves)
        if move != 'stand':
            if move == 'right' or move == 'left':
                distance = random.randint(100,(self.screenWidth*3)//4)
            else:
                distance = random.randint(100,(self.screenHeight*3)//4)
            self.randomMoveTimer.stop()
            self.walk(move, distance)
        print(move)
        

    def click_char(self):
        print("Hallo!")
        # self.walk('left', 300)

    def walk(self, direction, distance):
        self.starting_distance = distance
        self.current_direction = direction
        self._walkCheck()
        self.steps_left = self.starting_distance

        self._walkAnimate()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._walkStep)
        self.timer.start(4)
    
    def _walkAnimate(self):
        if self.current_direction == "stand":
            self.char.setStyleSheet("border-image: url(saka.png)")
        elif self.current_direction == "down" or self.current_direction == "up":
            self.char.setStyleSheet("border-image: url(./sakaback.png);")

    def _walkCheck(self):
        if self.current_direction == "down" and self.starting_distance > (self.screenHeight-50)-(self.posY+150):
            self.starting_distance = (self.screenHeight-50)-(self.posY+150)
        elif self.current_direction == "up" and self.posY - self.starting_distance < 0:
            self.starting_distance = self.posY
        elif self.current_direction == "right" and self.starting_distance > self.screenWidth-(self.posX+150):
            self.starting_distance = self.screenWidth-(self.posX+150)
        elif self.current_direction == "left" and self.posX - self.starting_distance < 0:
            self.starting_distance = self.posX

    def _walkStep(self):
        # print(self.posX, self.posY)
        if self.steps_left <= 0:
            self.timer.stop()
            self.current_direction = "stand"
            self._walkAnimate()
            self.randomMoveTimer.start(5000)
            return

        if self.current_direction == "right":
            self.posX += 1
        elif self.current_direction == "left":
            self.posX -= 1
        elif self.current_direction == "up":
            self.posY -= 1
        elif self.current_direction == "down":
            if self.steps_left > 0.9*self.starting_distance:
                self.posY += 1
            elif self.steps_left > 0.6*self.starting_distance:
                self.posY += 2
                self.steps_left -= 1
            else: 
                self.posY += 4
                self.steps_left -= 3
        
        self.setGeometry((int(self.posX)), int(self.posY), 150, 150)
        self.steps_left -= 1

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()
        self.randomMoveTimer.stop()
        self.timer.stop()

    def mouseMoveEvent(self, event):
        self.char.setStyleSheet("border-image: url(./sakaback.png);")
        delta = QPoint(event.globalPos() - self.oldPos)
        self.posX = self.x() + delta.x()
        self.posY = self.y() + delta.y()
        self.move(self.posX, self.posY)
        self.oldPos = event.globalPos()

    def mouseReleaseEvent(self, event):
        self.char.setStyleSheet("border-image: url(./saka.png);")
        self.randomMoveTimer.start(5000)

    def contextMenuEvent(self, event: QContextMenuEvent):
        contextMenu = QMenu(self)

        quitAction = contextMenu.addAction("Bye bye!")

        action = contextMenu.exec_(self.mapToGlobal(event.pos()))

        if action == quitAction:
            self.close()

        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    screen = app.primaryScreen()
    size = screen.size()

    window = DesktopPet(size)
    window.show()
    sys.exit(app.exec_())