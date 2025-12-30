import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QMenu
from PyQt5.QtGui import QContextMenuEvent
from PyQt5.QtCore import Qt, QTimer

class DesktopPet(QMainWindow):
    def __init__(self, screenSize):
        super().__init__()
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setWindowFlags(Qt.FramelessWindowHint)
        # self.setGeometry(screenSize.width() - 150,
                        # screenSize.height() - 200,
                        # 150, 150)
        self.posX = 800
        self.posY = 500

        self.setGeometry(self.posX, self.posY, 150, 150)

        self.char = QPushButton("", self)
        
        self.initUI()
        
        
    def initUI(self):
        self.char.setGeometry(0,0,150,150)
        self.char.setStyleSheet("border-image: url(saka.png);")
        
        self.char.clicked.connect(self.click_char)

    def click_char(self):
        print("Hallo!")
        self.move('right', 300)

    def move(self, direction, distance):
        self.starting_distance = distance
        self.steps_left = distance
        self.current_direction = direction

        self.timer = QTimer(self)
        self.timer.timeout.connect(self._moveStep)
        self.timer.start(1)
        
        # if direction == "right" or direction == "left":
        #     self.timer.start(10)
        # elif direction == "down":
            # for _ in range(distance//10):
            #     self.posY += 1
            #     self.setGeometry(self.posX, self.posY, 150, 150)
            # for _ in range((distance//20)*3):
            #     self.posY += 2
            #     self.setGeometry(self.posX, self.posY, 150, 150)
            # for _ in range(((distance//40)*6)):
            #     self.posY += 4
            #     self.setGeometry(self.posX, self.posY, 150, 150)

            # self.timer.start(10)
            # self.timer.start(1)
            # phase1 = self.steps_left//10
            # phase2 = (3*self.steps_left)//10
            # phase3 = (6*self.steps_left)//10
            # print(phase1, phase2, phase3)

            # self.steps_left = phase1
            # self.timer.start(8)
            # self.steps_left = phase2
            # self.timer.start(4)
            # self.steps_left = phase3
            # self.timer.start(2)
            # pass
            
        # elif direction == "up":
            # for _ in range(distance):
            #     self.posY -= 1
            #     self.setGeometry(self.posX, self.posY, 150, 150)
        
    
    def _moveStep(self):
        if self.steps_left <= 0:
            self.timer.stop()
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
                self.posY += 3
                self.steps_left -= 2
            else: 
                self.posY += 6
                self.steps_left -= 5
        
        self.setGeometry((int(self.posX)), int(self.posY), 150, 150)
        self.steps_left -= 1
                

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