import numpy as np
import matplotlib.pyplot as plt
import pyvista as pv
import scipy.interpolate as spi

# vtkファイルのパスリスト
filename0 = r'\\wsl.localhost\Ubuntu-20.04\home\hiroaki\sensitivity_measurement\RANS\2d_run\flowCart.vtk'
filename1 = r'\\wsl.localhost\Ubuntu-20.04\home\hiroaki\sensitivity_measurement\sigma_point02\flowCart.vtk'
filename2 = r'\\wsl.localhost\Ubuntu-20.04\home\hiroaki\sensitivity_measurement\sigma_point2\2d_run\flowCart.vtk'
filename3 = r'\\wsl.localhost\Ubuntu-20.04\home\hiroaki\sensitivity_measurement\sigma_1point0\2d_run\flowCart.vtk'
vtk_files = [filename0, filename1, filename2, filename3]

# セルデータのキー（例えば "cp" や "p" など）を指定
key = "p"

# グラフの色
colors = ["red", "blue", "green", "orange"]

# グラフのラベル
labels = ["RANS", "sigma=0.02", "sigma=0.2", "sigma=1.0"]

# 原点と半径を設定
origin = [0, 0, 0]
radius = 0.5

# 円周上の点の数
num_points = 10000

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

    # 線形補間
    interp_func = spi.interp1d(theta_deg, scalar_data_circumference, kind='linear')
    theta_deg_smooth = np.linspace(theta_deg.min(), theta_deg.max(), 100000)  # より滑らかな曲線を生成するために点を増やす
    scalar_data_circumference_smooth = interp_func(theta_deg_smooth)

    # グラフのプロット
    plt.plot(theta_deg_smooth, scalar_data_circumference_smooth, color=colors[i], label=labels[i])

plt.xlabel("Theta(deg)")
plt.ylabel(key)
plt.title(f"Distribution of {key} along the circular path @ R = {radius}")
plt.legend()
plt.savefig(r'\\wsl.localhost\Ubuntu-20.04\home\hiroaki\report\b4labmtg\0530\figures\ranscompareAtR05.png')
plt.show()
