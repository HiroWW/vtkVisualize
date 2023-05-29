import pyvista as pv

# vtkファイルの読み込み
filename = r'\\wsl.localhost\Ubuntu-20.04\home\hiroaki\sensitivity_measurement\RANS\2d_run\flowCart.vtk'
# filename = r'\\wsl.localhost\Ubuntu-20.04\home\hiroaki\sensitivity_measurement\sigma_point02\2d_run\flowCart.vtk'
# filename = r'\\wsl.localhost\Ubuntu-20.04\home\hiroaki\sensitivity_measurement\sigma_point02\flowCart.vtk'
mesh = pv.read(filename)

# 表示倍率の設定
# magnification = 5.0  #default
magnification = 20.0 #upscale 
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
# p.show()
print("end plot")

# 画像の保存
# output_filename = r'C:\Users\hiroa\Documents\vtkVisualize\images\0p02.png'
output_filename = r'\\wsl.localhost\Ubuntu-20.04\home\hiroaki\report\b4labmtg\0530\figures\images\rans_upscale.png'
p.screenshot(output_filename)
print("sucessfully saved")
