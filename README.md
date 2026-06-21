# desktop-cute

macOSでのみ対応しています。pyobjc使用箇所(qttransparent,macosmouse)を変更することでwindows等でも使える可能性があります

native-live2d: live2dキャラを表示
web-spine: spineを表示
web-3d-pmx: pmxファイルまたは他の3dファイルを表示

## native-live2d

必要なライブラリ:
```
live2d-py
pyopengl
pyqt6
pyobjc
```

```sh
python3 main_native.py {id}
```

## web-spine & web-3d-pmx

必要なライブラリ:
```
pyqt6-webengine
pyqt6
pyobjc
```

必要なコマンド:
```
esbuild (または他のtypescript compiler)
npm (または他のパッケージマネージャ)
```


```sh
python3 main_3dwebv.py
```


```sh
python3 main_spinewebv.py
```