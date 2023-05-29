import numpy as np
import matplotlib.pyplot as plt
import pyvista as pv

# vtkファイルのパスリスト
filename0 = r'\\wsl.localhost\Ubuntu-20.04\home\hiroaki\sensitivity_measurement\RANS\2d_run\flowCart.vtk'
filename1 = r'\\wsl.localhost\Ubuntu-20.04\home\hiroaki\sensitivity_measurement\sigma_point1\2d_run\flowCart.vtk'
filename2 = r'\\wsl.localhost\Ubuntu-20.04\home\hiroaki\sensitivity_measurement\sigma_2point5\2d_run\flowCart.vtk'
vtk_files = [filename0, filename1, filename2]

# セルデータのキー（例えば "cp" や "p" など）を指定
key = "p"

# グラフの色
colors = ["red", "blue", "green"]

# グラフのラベル
labels = ["RANS","sigma=0.2","sigma=2.5"]

# 原点と半径を設定
origin = [0, 0, 0]
radius = 2.0

# 円周上の点の数
num_points = 100

# 円周上の点を生成
theta = np.linspace(0, 2 * np.pi, num_points, endpoint=False)
x = origin[0] + radius * np.cos(theta)
y = origin[1] + radius * np.sin(theta)
z = origin[2] * np.ones_like(theta)

# 円周上の点の座標を結合
points = np.column_stack((x, y, z))

# グラフのプロット
plt.figure()

for i, vtk_file in enumerate(vtk_files):
    # vtkファイルの読み込み
    mesh = pv.read(vtk_file)
    scalar_data = mesh.cell_data.get_array(key)

    # 円周上のセルのインデックスを取得
    cell_indices = mesh.find_closest_cell(points)

    # 円周上のセルデータを取得
    scalar_data_circumference = scalar_data[cell_indices]

    # thetaの度数法への変換
    theta_deg = np.degrees(theta)

    # グラフのプロット
    plt.plot(theta_deg, scalar_data_circumference, color=colors[i], label=labels[i])

plt.xlabel("Theta(deg)")
plt.ylabel(key)
plt.title(f"Distribution of {key} along the circular path")
plt.legend()
plt.show()
