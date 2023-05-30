import pyvista as pv
import numpy as np
import matplotlib.pyplot as plt

# バイナリvtkファイルの読み込み
# filename = r'\\wsl.localhost\Ubuntu-20.04\home\hiroaki\sensitivity_measurement\RANS\2d_run\flowCart.vtk'
filename = r'\\wsl.localhost\Ubuntu-20.04\home\hiroaki\sensitivity_measurement\sigma_point2\2d_run\flowCart.vtk'
# バイナリデータをPyVistaメッシュとして読み込む
mesh = pv.read(filename)

# カラーマップの範囲を固定
minimum_value = 0.6  # カラーマップの最小値
maximum_value = 0.735  # カラーマップの最大値

# 可視化
p = pv.Plotter()
p.add_mesh(mesh, scalars="p", cmap="jet", clim=[minimum_value, maximum_value])
magnification = 20.0 #upscale 
p.camera.zoom(magnification)
# カメラの設定（適宜調整してください）
p.camera_position = [(0, 0, 100), (0, 0, 0), (0, 1, 0)]
p.camera_set = True

# プロットの実行
p.show()
