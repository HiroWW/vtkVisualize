# Paraviewのモジュールをインポート
from paraview.simple import *

# コマンドライン引数の取得
vtk_file = sys.argv[1]
magnification = float(sys.argv[2])

# vtkファイルの読み込み
reader = LegacyVTKReader(FileNames=[vtk_file])

# レンダービューの作成
render_view = CreateRenderView()

# レンダービューに表示するデータソースを設定
render_view.AddRepresentation(None, reader)

# 表示倍率の設定
render_view.CameraZoom(magnification)

# 等圧線の追加
contour = Contour(Input=reader)
contour.ContourBy = ['POINTS', 'Pressure']
contour.Isosurfaces = [0.5]  # 等圧線の値を指定

# 表示プロパティの設定
contour_display = Show(contour, render_view)
contour_display.ColorArrayName = ['POINTS', '']
contour_display.Opacity = 0.5

# ビューのアップデート
render_view.Update()

# 画像の保存
SaveScreenshot(r'\\wsl.localhost\Ubuntu-20.04\home\hiroaki\report\b4labmtg\0530\figures\images\rans_upscale.png', view=render_view)
