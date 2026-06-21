from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from PyQt6.QtCore import QTimer, Qt, QPoint
from macosmouse import get_global_mouse_position
import objc

class TransparentWindow(QMainWindow):
    MOUSE_TIMER = 50

    def __init__(self):
        super().__init__()
        self._is_transparent = True

        self.setWindowFlags(
            (Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowTransparentForInput |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.BypassWindowManagerHint |
            Qt.WindowType.NoDropShadowWindowHint)
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.enable_all_spaces_macos()

        # マウス位置監視タイマー
        self.mouse_timer = QTimer(self)
        self.mouse_timer.timeout.connect(self.check_mouse_range)
        self.mouse_timer.start(self.MOUSE_TIMER)

    def mouseMoveMacos(self, x:int, y: int):
        pass


    hitrange = 5

    def calc_mouse_range_focusout(self,gx,gy,cx,cy,w,h):
        return abs(gx - cx) < w//2 and abs(gy - cy) < h//2
    
    def calc_mouse_range_focus(self,gx,gy,cx,cy,w,h):
        return abs(gx - cx) < w//(self.hitrange*2) and abs(gy - cy) < h//(self.hitrange*2)

    def check_mouse_range(self):
        gx, gy = get_global_mouse_position()
        rect = self.geometry()

        # mouseMoveEvent 代用
        self.mouseMoveMacos(-rect.topLeft().x() + gx, -rect.topLeft().y() + gy)

        cx, cy = rect.center().x(), rect.center().y()
        w, h = rect.width(), rect.height()

        in_range = self.calc_mouse_range_focus(gx,gy,cx,cy,w,h)
        in_wrange = self.calc_mouse_range_focusout(gx,gy,cx,cy,w,h)

        if in_range and self._is_transparent:
            self.set_transparency(False)
        elif not in_wrange and not self._is_transparent:
            self.set_transparency(True)

    def set_transparency(self, transparent: bool):
        self._is_transparent = transparent
        flags = self.windowFlags()
        if transparent:
            flags |= Qt.WindowType.WindowTransparentForInput
        else:
            flags &= ~Qt.WindowType.WindowTransparentForInput
        
        self.setWindowFlags(flags)
        self.show()

    def show(self):
        super().show()
        self.enable_all_spaces_macos()

    _drag_pos = None
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if self._drag_pos is not None:
            new_pos = event.globalPosition().toPoint() - self._drag_pos
            self.move(new_pos)
            event.accept()

    def mouseReleaseEvent(self, event):
        self._drag_pos = None
        event.accept()

    def enable_all_spaces_macos(self):
        
        # 1. Qtの内部的なウィンドウハンドル（WId）を取得
        win_id = int(self.winId())
        
        # 2. ctypes / objc を使って NSWindow オブジェクトに変換
        # PyQt6のwinId()は直接NSWindowのポインタ、またはNSViewのポインタを返すため、
        # 環境に応じてNSWindowインスタンスをラップします。
        ns_view = objc.objc_object(c_void_p=win_id)
        ns_window = ns_view.window()
        
        if ns_window:
            # 3. すべてのSpace（仮想デスクトップ）に参加する挙動をセット
            ns_window.setCollectionBehavior_(
                ns_window.collectionBehavior() | 1
            )


class TransparentWindowNoMoving(QMainWindow):
    MOUSE_TIMER = 50

    def __init__(self):
        super().__init__()
        self._is_transparent = True

        self.setWindowFlags(
            (Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowTransparentForInput | 
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.BypassWindowManagerHint |
            Qt.WindowType.NoDropShadowWindowHint)
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.enable_all_spaces_macos()

        # マウス位置監視タイマー
        self.mouse_timer = QTimer(self)
        self.mouse_timer.timeout.connect(self.check_mouse_range)
        self.mouse_timer.start(self.MOUSE_TIMER)

    def mouseMoveMacos(self, x:int, y: int):
        pass

    def check_mouse_range(self):
        gx, gy = get_global_mouse_position()
        rect = self.geometry()
        # mouseMoveEvent 代用
        self.mouseMoveMacos(-rect.topLeft().x() + gx, -rect.topLeft().y() + gy)

    def set_transparency(self, transparent: bool):
        if self._is_transparent == transparent:
            return
        
        self._is_transparent = transparent
        flags = self.windowFlags()
        if transparent:
            flags |= Qt.WindowType.WindowTransparentForInput
        else:
            flags &= ~Qt.WindowType.WindowTransparentForInput
        
        self.setWindowFlags(flags)
        self.show()

    def show(self):
        super().show()
        self.enable_all_spaces_macos()

    def enable_all_spaces_macos(self):
        
        # 1. Qtの内部的なウィンドウハンドル（WId）を取得
        win_id = int(self.winId())
        
        # 2. ctypes / objc を使って NSWindow オブジェクトに変換
        # PyQt6のwinId()は直接NSWindowのポインタ、またはNSViewのポインタを返すため、
        # 環境に応じてNSWindowインスタンスをラップします。
        ns_view = objc.objc_object(c_void_p=win_id)
        ns_window = ns_view.window()
        
        if ns_window:
            # 3. すべてのSpace（仮想デスクトップ）に参加する挙動をセット
            ns_window.setCollectionBehavior_(
                ns_window.collectionBehavior() | 1
            )