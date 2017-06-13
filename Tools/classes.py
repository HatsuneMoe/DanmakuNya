from PyQt5.QtWidgets import QDesktopWidget
from PyQt5.QtGui import QFont, QPainterPath, QPainter, QColor


class Message:
    def __init__(self, message, b_x, b_y, size=48, fonts='微软雅黑'):
        width = QDesktopWidget().screenGeometry().width() + \
                size * len(message)
        self.speed = 3 if width / 180 < 14 else width / 720
        print(self.speed)

        self.message = message
        self.b_x = b_x
        self.b_y = b_y
        self.fonts = fonts
        self.size = size
        self.m_path = QPainterPath()

    def gen_path(self):
        self.m_path.addText(self.b_x, self.b_y, QFont(self.fonts, self.size), self.message)

        return {
            'path': self.m_path,
            'speed': self.speed,
            'len': len(self.message)
        }


class MyBrush:
    def __init__(self, color='#ffffff', border_color='#000000'):
        self.color = color
        self.border_color = border_color
        self.qp = QPainter()

    def draw(self, them, item):
        self.qp.begin(them)
        self.qp.setRenderHint(QPainter.Antialiasing)
        self.qp.setBrush(QColor(self.color))
        self.qp.setPen(QColor(self.border_color))
        self.qp.drawPath(item['path'])
        item['path'].translate(-item['speed'], 0)
        self.qp.end()

