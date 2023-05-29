import pyvista as pv

# vtkファイルの読み込み
filename = r'\\wsl.localhost\Ubuntu-20.04\home\hiroaki\sensitivity_measurement\sigma_point2\2d_run\flowCart.vtk'
mesh = pv.read(filename)

# 表示倍率の設定
magnification = 10.0

# 表示スカラーの指定
scalar_data = mesh.cell_data.get_array("p")

# 表示ウィンドウの作成
p = pv.Plotter()

# メッシュを表示
p.add_mesh(mesh, scalars=scalar_data, render_points_as_spheres=True)

# 表示倍率の設定
p.camera.zoom(magnification)

# カメラのポジションを設定（上から見た視点）
p.camera_position = [(0, 0, 100), (0, 0, 0), (0, 1, 0)]
p.camera_set = True

# プロットの実行
print("begin plot")
p.show(interactive=False)
#p.show()
print("end plot")

# 画像の保存
output_filename = r'C:\Users\hiroa\Documents\vtkVisualize\images\image.png'
p.screenshot(output_filename)
print("sucessfully saved")
