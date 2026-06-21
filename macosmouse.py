import time
from Quartz import CGEventCreate, CGEventGetLocation

def get_global_mouse_position() -> tuple[float,float]:
    # システムの現在のイベントソースからマウスイベントを生成
    event = CGEventCreate(None)
    # そのイベントからグローバル座標（画面左上基準）を取得
    location = CGEventGetLocation(event)
    return location.x, location.y
