# 同じ値が連続した場合は削除したうえで線形補完を行う
# ransの分布中心を移動させてどこでALＭが一番近似しているのかを調査する

import numpy as np
import matplotlib.pyplot as plt
import pyvista as pv
import scipy.interpolate as spi

# vtkファイルのパスリスト
RANS = r'\\wsl.localhost\Ubuntu-20.04\home\hiroaki\sensitivity_measurement\RANS\2d_run\flowCart.vtk'
ALM = r'\Users\hiroa\Documents\CFD_experiment\0619center_of_gauss\results\vtk\flowCart_0.05d0.vtk'

# セルデータのキー（例えば "cp" や "p" など）を指定
key = "p"

# グラフの色
# カラーマップの取得
cmap = plt.get_cmap('tab10')

# カラーリストの生成
colors = [cmap(i) for i in range(6)]
#colors = ["red", "blue", "green", "orange", "yellow", "red"]

# グラフのラベル
labels = ["0.0", "0.25", "0.5", "0.75", "1.0", "ALM"]

radList = [0.5, 1.5, 3.0]
for j in range(3):
    # 原点と半径を設定
    origin = [0, 0, 0]
    radius = radList[j]

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

    centers = [0.0, 0.25, 0.5, 0.75, 1.0]
    for i, center in enumerate(centers):
        # 円の中心の移動
        origin[0] = center
        x = origin[0] + radius * np.cos(theta)
        points = np.column_stack((x, y, z)) 

        mesh = pv.read(RANS)
        scalar_data = mesh.cell_data.get_array(key)

        # 円周上のセルのインデックスを取得
        cell_indices = mesh.find_closest_cell(points)

        # 円周上のセルデータを取得
        scalar_data_circumference = scalar_data[cell_indices]

        # thetaの度数法への変換
        theta_deg = np.degrees(theta)

        # 同じ値が連続している箇所を削除
        indices_to_keep = np.diff(scalar_data_circumference) != 0
        scalar_data_circumference = scalar_data_circumference[:-1][indices_to_keep]
        theta_deg = theta_deg[:-1][indices_to_keep]

        # 線形補間
        interp_func = spi.interp1d(theta_deg, scalar_data_circumference, kind='linear')
        theta_deg_smooth = np.linspace(theta_deg.min(), theta_deg.max(), 10000)  # より滑らかな曲線を生成するために点を増やす
        scalar_data_circumference_smooth = interp_func(theta_deg_smooth)

        # グラフのプロット
        plt.plot(theta_deg_smooth, scalar_data_circumference_smooth, color=colors[i], label=labels[i])

    ###########################
    ## ALMに対してプロットを行う
    ###########################

    # 円周上の点を再生成
    theta = np.linspace(0, 2 * np.pi, num_points, endpoint=False)
    x = origin[0] + radius * np.cos(theta)
    y = origin[1] + radius * np.sin(theta)
    z = origin[2] * np.ones_like(theta)
    # 円周上の点の座標を結合
    points = np.column_stack((x, y, z))

    mesh = pv.read(ALM)
    scalar_data = mesh.cell_data.get_array(key)

    # 円周上のセルのインデックスを取得
    cell_indices = mesh.find_closest_cell(points)

    # 円周上のセルデータを取得
    scalar_data_circumference = scalar_data[cell_indices]

    # thetaの度数法への変換
    theta_deg = np.degrees(theta)

    # 同じ値が連続している箇所を削除
    indices_to_keep = np.diff(scalar_data_circumference) != 0
    scalar_data_circumference = scalar_data_circumference[:-1][indices_to_keep]
    theta_deg = theta_deg[:-1][indices_to_keep]

    # 線形補間
    interp_func = spi.interp1d(theta_deg, scalar_data_circumference, kind='linear')
    theta_deg_smooth = np.linspace(theta_deg.min(), theta_deg.max(), 100000)  # より滑らかな曲線を生成するために点を増やす
    scalar_data_circumference_smooth = interp_func(theta_deg_smooth)

    # グラフのプロット
    plt.plot(theta_deg_smooth, scalar_data_circumference_smooth, color=colors[5], label=labels[5])



    plt.xlabel("Theta(deg)")
    plt.ylabel(key)
    plt.title(f"Distribution of {key} along the circular path @ R = {radius}")
    plt.legend()
    plt.savefig(f'\\\wsl.localhost\\Ubuntu-20.04\\home\\hiroaki\\report\\b4labmtg\\0620\\figures\\ranscompareAtR{radius}.png')
    print(f"save complete at {radius}")
    #plt.show()
