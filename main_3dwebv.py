import sys,subprocess,os,json,time
from PyQt6.QtCore import Qt, QUrl, QEvent, QObject, pyqtSlot, pyqtSignal
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebChannel import QWebChannel

from qttransparent import TransparentWindowNoMoving

TARGET = 0

import httpserver
server = httpserver.server("./3dweb/")

subprocess.call(["esbuild", "--bundle", "./3dweb/index.ts", "--outfile=./3dweb/index.js", "--define:TARGET=" + str(TARGET)])

# wait
time.sleep(1)

LEFT = 0
WIDTH = 1680

TOP = 0
HEIGHT = 1050

# 1. JavaScriptからのメッセージを受け取るためのブリッジクラス
class WebBridge(QObject):
    # PythonからJSへメッセージを送るためのカスタムシグナル
    messageReceivedFromPython = pyqtSignal(str)

    def __init__(self):
        super().__init__()

    # JSから呼び出されるスロット（引数の型を明示する）
    @pyqtSlot(str)
    def postMessage(self, message):
        window.mika_pos = json.loads(message)


class WebViewMikaWindow(TransparentWindowNoMoving):
    mika_pos = {"x":0,"y":0}
    MOUSE_TIMER = 33

    def __init__(self):
        super().__init__()
        self.setGeometry(LEFT, TOP, WIDTH-LEFT, HEIGHT-TOP)
        self.web_view = QWebEngineView()
        self.channel = QWebChannel()
        self.bridge = WebBridge()

        self.channel.registerObject("pyBridge", self.bridge)
        self.web_view.page().setWebChannel(self.channel)

        self.web_view.page().setBackgroundColor(Qt.GlobalColor.transparent)
        self.web_view.setUrl(QUrl("http://127.0.0.1:9090/index.html"))
        self.setCentralWidget(self.web_view)
    
    def mouseMoveMacos(self, x, y):
        #print(f"{x} / {y} : {self.mika_pos["x"]} / {self.mika_pos["y"]}")
        if (self._is_transparent) and abs(x-self.mika_pos["x"])<20 and abs(y-self.mika_pos["y"])<20:
            self.set_transparency(False)
        elif (not self._is_transparent) and abs(x-self.mika_pos["x"])>100 and abs(y-self.mika_pos["y"])>100:
            self.set_transparency(True)
        elif self._is_transparent:
            self.bridge.messageReceivedFromPython.emit('{"x":'+str(x)+',"y":'+str(y)+'}')
        return


app = QApplication(sys.argv)
window = WebViewMikaWindow()
window.show()

app.exec()
server.kill()
sys.exit()