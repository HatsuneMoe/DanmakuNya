import sys
from PyQt5.QtGui import QPalette
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtNetwork import QTcpSocket
from PyQt5.QtWidgets import QWidget, QApplication, QDesktopWidget

from Tools.classes import Message, MyBrush


class MainFrame(QWidget):
    def __init__(self, ip='127.0.0.1', port=8888):
        super().__init__(flags=(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint ))

        print("test: ", Qt.WindowStaysOnTopHint)
        print("test: ", (Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint))

        self.q_rect = QDesktopWidget().screenGeometry()
        self.ip = ip
        self.port = int(port)

        self.interval = 15
        self.fonts_size = 48

        self.danmaku_list = list()
        self.line_list = [None for _ in range(0, self.q_rect.height() // (self.fonts_size + self.interval))]
        self.brush = MyBrush()
        self.timer = QTimer()
        self.socket = QTcpSocket(self)

        self.set_transparent()
        self.init_ui()
        self.init_net()
        self.set_timer()

    def set_timer(self):
        self.timer.setInterval(16)
        self.timer.start()
        self.timer.timeout.connect(lambda: self.update() if self.danmaku_list else None)

    def set_transparent(self):
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)

        palette = self.palette()
        palette.setBrush(QPalette.Base, Qt.transparent)
        self.setPalette(palette)

    def init_net(self):
        self.socket.readyRead.connect(self.data_received)
        self.socket.connected.connect(self.connected)
        self.socket.connectToHost(self.ip, self.port)

    def init_ui(self):
        self.setGeometry(self.q_rect)
        self.setWindowTitle('Danmaku')
        self.show()

    def data_received(self):
        if self.socket.bytesAvailable() > 0:
            length = self.socket.bytesAvailable()
            msg = self.socket.read(length).decode('utf-8')
            print(msg)

            if msg[:5] == 'ika__':
                msg = msg[5:-1] if msg[:-1] != '\n' else msg[5:]
                danmaku = self.dispatch_line(Message(msg, self.q_rect.width(), 0, self.fonts_size).gen_path())

                self.danmaku_list.append(danmaku)

    def disconnected(self):
        pass  # todo: retry

    def connected(self):
        print('connecting...')
        self.socket.writeData('conn\n'.encode('utf-8'))
        print(self.socket.state())

    def dispatch_line(self, danmaku):
        planck = self.fonts_size + self.interval

        for item in self.line_list:
            if not item:
                danmaku['path'].translate(0, planck * (self.line_list.index(item) + 1))
                self.line_list[self.line_list.index(item)] = danmaku
                break
            else:
                speed_diff = danmaku['speed'] - item['speed']
                distance = self.q_rect.width() - item['path'].currentPosition().x() - item['len'] * self.fonts_size
                print(speed_diff, " dis:", distance)

                if speed_diff <= 0 < distance:
                    danmaku['path'].translate(0, planck * (self.line_list.index(item) + 1))
                    self.line_list[self.line_list.index(item)] = danmaku
                    break
        return danmaku

    def paintEvent(self, event):
        for item in self.danmaku_list[::-1]:
            self.brush.draw(self, item)
            now = item['path'].currentPosition().x() + item['path'].length()
            if now < 0:
                self.danmaku_list.remove(item)
                if item in self.line_list:
                    self.line_list[self.line_list.index(item)] = None
                del item


if __name__ == '__main__':
    print(sys.argv)
    app = QApplication(sys.argv)
    ex = MainFrame(sys.argv[1], sys.argv[2]) if len(sys.argv) == 3 else MainFrame()
    sys.exit(app.exec_())
