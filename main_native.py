import sys

sys.path.append("/Users/211601aok/kpc/desktop/.venv/lib/python3.12/site-packages")

from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from PyQt6.QtCore import QTimer, Qt, QPoint
import live2d.v3 as live2d
import time # 追加
from macosmouse import get_global_mouse_position
from qttransparent import TransparentWindow

TARGET = int(sys.argv[1]) # or 210502

WIDTH = 1680
LEFT = 1300

TOP = 400
HEIGHT = 1050

RANGEX = 50
RANGEY = 100

WRANGEX = (WIDTH-LEFT)//2
WRANGEY = (HEIGHT-TOP)//2

class Live2DWidget(QOpenGLWidget):
    def __init__(self):
        super().__init__()
        self.model: live2d.LAppModel | None = None
        self.setMouseTracking(True)
        self.start_time = time.time()
        # 座標保持用の変数を追加
        self._last_mouse_pos = None 

    def initializeGL(self):
        print(f"[{time.time() - self.start_time:.2f}s] initializeGL start")
        live2d.init()
        live2d.glInit()
        
        self.model = live2d.LAppModel()
        model_path = f"./image_native/live2d_v4/{TARGET}/model.model3.json"
        print(f"[{time.time() - self.start_time:.2f}s] Loading model: {model_path}")

        self.model.LoadModelJson(model_path)
        self.model.Resize(self.width(), self.height())
        self.model.SetExpression("mtn_ex_010.exp3.json")

        print(f"[{time.time() - self.start_time:.2f}s] model loaded instance: {self.model}")
        
        self.startTimer(33) 

    def paintGL(self):
        if self.model is None:
            return
            
        live2d.clearBuffer(0, 0, 0, 0)
        
        # paintGLの中で一回だけDragを行う
        if self._last_mouse_pos is not None:
            self.model.Drag(*self._last_mouse_pos)
            # 頻繁なDragを抑制したい場合はここでNoneに戻すことも検討
        
        self.model.Update()
        self.model.Draw()

    #def mouseMoveEvent(self, event):
    #    # ここではライブラリを呼ばず、座標の保存だけにする
    #    pos = event.position()
    #    # self._last_mouse_pos = (pos.x(), pos.y())
    #    # 親ウィンドウへのイベント伝播を許可（ドラッグ移動用）
    #    event.ignore()

    def mousePressEvent(self, a0):
        self.model.StartRandomMotion("Motion")
        # 親ウィンドウへイベントを伝播させ、ドラッグ移動を可能にする
        a0.ignore()

    def timerEvent(self, a0: None) -> None:
        self.update()

    def closeEvent(self, event):
        print(f"[{time.time() - self.start_time:.2f}s] closeEvent")
        self.model = None
        live2d.dispose()
        event.accept()

class MainWindow(TransparentWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(LEFT, TOP, WIDTH-LEFT, HEIGHT-TOP)

        self.gl_widget = Live2DWidget()
        self.setCentralWidget(self.gl_widget)
    
    def mouseMoveMacos(self, x, y):
        self.gl_widget._last_mouse_pos = (x, y)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())