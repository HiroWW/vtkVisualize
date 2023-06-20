# vtkVisualize
CFDの計算結果として出力されるvtkファイルをPythonで操作するためのスクリプト群である。

root
├─ Visualizer
│   ├─ main.py
│   └─ README.md
├─ CircleInterpolateMoveCenter
│   ├─ main.py
│   └─ README.md
└─ Others
      ├─ moveCenter.py
      └─ README.md

### Visualizer

固定の縮小率・視点でvtkファイルを読み込み、可視化して、指定のパスに保存する。

### Circle Interpolate

流れ場のうえに円を考え、その円周上の各点に最も近いセルの状態量を縦軸、円周上の点を指定する回転角θを横軸にとってプロットする。

複数のプロットを重ね合わせることで、複数の解析結果の流れ場の近似を定性的に比較することが可能。

各点をスプライン補完して曲線を描画している。

### Others

その他細かいファイル群。

#### move center

基本的にはCircle Interpolateと同じ。RANS側の円の中心を移動させ、ALMにおける分布関数の中心として最も適した点を探索する。
