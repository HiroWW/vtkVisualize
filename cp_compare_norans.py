import numpy as np
import matplotlib.pyplot as plt
import pyvista as pv

# VTKファイルのファイル名リスト
filename1 = r'\\wsl.localhost\Ubuntu-20.04\home\hiroaki\sensitivity_measurement\sigma_point2\2d_run\flowCart.vtk'
filename2 = r'\\wsl.localhost\Ubuntu-20.04\home\hiroaki\sensitivity_measurement\sigma_1point3\2d_run\flowCart.vtk'
filename3 = r'\\wsl.localhost\Ubuntu-20.04\home\hiroaki\sensitivity_measurement\sigma_2point5\2d_run\flowCart.vtk'
filenames = [filename1, filename2,filename3]
labels = ["sigma=0.2","sigma=1.3","sigma=2.5"]
# グラフのプロット用の配列
data = []

# ファイルごとにデータを取得
for filename in filenames:
    # VTKファイルの読み込み
    mesh = pv.read(filename)
    
    # セルデータのスカラーデータを取得
    scalar_data = mesh.cell_data.get_array("p")
    
    # データを配列に追加
    data.append(scalar_data)

# 原点と半径を設定
origin = [0, 0, 0]
radius = 1.0

# 円周上の点の数
num_points = 100

# 円周上の点を生成
theta = np.linspace(0, 2*np.pi, num_points, endpoint=False)
x = origin[0] + radius * np.cos(theta)
y = origin[1] + radius * np.sin(theta)
z = origin[2] * np.ones_like(theta)

# 円周上の点の座標を結合
points = np.column_stack((x, y, z))

# グラフのプロット
for i, scalar_data in enumerate(data):
    # 円周上のセルのインデックスを取得
    cell_indices = mesh.find_closest_cell(points)
    
    # 円周上のセルのpを取得
    p_values = scalar_data[cell_indices]
    
    # ラジアンから度数に変換
    theta_deg = np.degrees(theta)
    
    # グラフのプロット
    plt.plot(theta_deg, p_values, label=labels[i])

plt.xlabel("Theta (degrees)")
plt.ylabel("p")
plt.title("Comparison of p Distribution along the Circular Path")
plt.legend()
plt.savefig(r'C:\Users\hiroa\Documents\vtkVisualize\images\graph.png')
plt.show()