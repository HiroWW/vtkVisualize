import numpy as np
import matplotlib.pyplot as plt
import pyvista as pv
import scipy.interpolate as spi
import os 
import argparse

# -------------------------------------------------------------------------
#                       parameter table  (CHANGE HERE)                    
# グラフのラベル
# # fine
# labels = ["RANS","mesh=0.01","mesh=0.0125","mesh=0.025"]
# coarse
labels = ["RANS","mesh=0.05","mesh=0.1","mesh=0.2"]
# # all
# labels = ["RANS","mesh=0.01","mesh=0.05","mesh=0.1"]
# 半径
radiuses = [0.5, 1.5, 3.0]
# 原点と半径を設定
origin = [0.0, 0, 0]
# 無次元化用物性パラメータ
u = 0.2
rho = 1.293
# -------------------------------------------------------------------------

print("-------------------------------------------------------------------")
print("                        2d CFD analizer                            ")
print("-------------------------------------------------------------------")

print("Do you want to show the plot result ?")
print("Input here : y/n")
flagShow = input()

print("Do you use RANS vtk data ?")
print("Input here : y/n")
flagRANS = input()
if (flagRANS == "y"):
  print("-------------------------------------------------------------------")
  print("                          MODE : RANS                              ")
  print("            * Be carefull to put RANS data at first *              ")
  print("-------------------------------------------------------------------")


def collect_vtk_files(directory):
    vtk_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".vtk"):
                vtk_files.append(os.path.join(root, file))
    # 名前順に並び替え
    vtk_files.sort()
    return vtk_files

# コマンドライン引数の解析
parser = argparse.ArgumentParser()
parser.add_argument("directory_name", help="Directory containing vtk files")
args = parser.parse_args()

# ディレクトリのパス
directory = os.path.abspath(args.directory_name)

# vtkファイルのパスを収集
vtk_files = collect_vtk_files(directory)

# パスの確認
print("-------------------------------------------------------------------")
print("Data readed :")
for vtk_file in vtk_files:
    print(vtk_file)
print("-------------------------------------------------------------------")
# セルデータのキー（例えば "cp" や "p" など）を指定
key = "p"

# グラフの色
cmap = plt.get_cmap('tab10')
colors = [cmap(i) for i in range(len(vtk_files))]

# 円周上の点の数
num_points = 1000

# 円周上の点を生成
theta = np.linspace(0, 2 * np.pi, num_points, endpoint=False)

for j, radius in enumerate(radiuses):
    # グラフのプロット
    plt.figure()    
    x = origin[0] + radius * np.cos(theta)
    y = origin[1] + radius * np.sin(theta)
    z = origin[2] * np.ones_like(theta)
    # 円周上の点の座標を結合
    points = np.column_stack((x, y, z))
    for i, vtk_file in enumerate(vtk_files):
        # vtkファイルの読み込み
        mesh = pv.read(vtk_file)
        scalar_data = mesh.cell_data.get_array(key)
        scalar_data_u = mesh.cell_data.get_array("u")
        scalar_data_v = mesh.cell_data.get_array("v")
        scalar_data_rho = mesh.cell_data.get_array("rho")
        print("------ U -----")
        print(scalar_data_u)
        print("----  rho ----")
        print(scalar_data_rho)
        print("------ p ------")
        print(scalar_data)

        # 円周上のセルのインデックスを取得
        cell_indices = mesh.find_closest_cell(points)

        # 円周上のセルデータを取得
        scalar_data_circumference = scalar_data[cell_indices]
        # 無次元化
        scalar_data_circumference = scalar_data_circumference / (1/2 * u**2 * rho)

        # thetaの度数法への変換
        theta_deg = np.degrees(theta)

        # 同じ値が連続している箇所を削除
        indices_to_keep = np.diff(scalar_data_circumference) != 0
        scalar_data_circumference = scalar_data_circumference[:-1][indices_to_keep]
        theta_deg = theta_deg[:-1][indices_to_keep]

        if (i == 0 and flagRANS == "y"):
          # RANSのデータは線形補完
          interp_func = spi.interp1d(theta_deg, scalar_data_circumference, kind="linear")
          theta_deg_smooth = np.linspace(theta_deg.min(), theta_deg.max(), 1000)
          scalar_data_circumference_smooth = interp_func(theta_deg_smooth)
        else :
          # ALMのデータはスプライン補完
          tck = spi.splrep(theta_deg, scalar_data_circumference)
          theta_deg_smooth = np.linspace(theta_deg.min(), theta_deg.max(), 100000)  # より滑らかな曲線を生成するために点を増やす
          scalar_data_circumference_smooth = spi.splev(theta_deg_smooth, tck)

        # グラフのプロット
        plt.plot(theta_deg_smooth, scalar_data_circumference_smooth, color=colors[i], label=labels[i])

    plt.xlabel("Theta(deg)")
    plt.ylabel(key)
    plt.title(f"Distribution of {key} along the circular path @ R = {radius}")
    plt.legend()
    if (flagShow == "y"):
        plt.show()  
    plt.savefig(f"images/distribution_of_{key}_along_the_circular_path_at_{radius}_in_fine.png")
    print(f"plot complete @ R = {radius}")


print("-------------------------------------------------------------------")
print("                          All COMPLETE                             ")
print("-------------------------------------------------------------------")