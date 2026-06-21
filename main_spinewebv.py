import sys,subprocess,os,time
from PyQt6.QtCore import Qt, QUrl, QEvent
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt6.QtWebEngineWidgets import QWebEngineView
from qttransparent import TransparentWindow

TARGET = "b"

subprocess.call(["esbuild", "--bundle", "./spineweb/index_s.ts", "--outfile=./spineweb/index_s.js"])
subprocess.call(["esbuild", "--bundle", "./spineweb/index_b.ts", "--outfile=./spineweb/index_b.js"])

import httpserver
server = httpserver.server("./spineweb/")
time.sleep(1)

HEIGHT = 1050
WIDTH = 1680

if TARGET == "b":
    TOP = 500
    LEFT = 1000
else:
    TOP = 400
    LEFT = 1350

class WebViewWindow(TransparentWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(LEFT, TOP, WIDTH-LEFT, HEIGHT-TOP)
        self.web_view = QWebEngineView()
        self.web_view.page().setBackgroundColor(Qt.GlobalColor.transparent)
        self.web_view.setUrl(QUrl("http://127.0.0.1:9090/index_"+TARGET+".html"))
        self.setCentralWidget(self.web_view)
        self.web_view.focusProxy().installEventFilter(self)

    def eventFilter(self, watched, event):
        # マウスボタンが押されたイベントをキャッチ
        if (event.type() == QEvent.Type.MouseButtonPress):
            self.mousePressEvent(event)
            return False
        if (event.type() == QEvent.Type.MouseMove):
            self.mouseMoveEvent(event)
            return False
        if (event.type() == QEvent.Type.MouseButtonRelease):
            self.mouseReleaseEvent(event)
            return False
        return super().eventFilter(watched, event)



app = QApplication(sys.argv)
window = WebViewWindow()

window.show()
app.exec()
server.kill()
sys.exit()