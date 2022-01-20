# CreateSimpleCurve

Xform内の複数のSphereを使用し、Spbereをスプライン補間したチューブ形状を作成します。     

## 使い方

複数のSphereを配置します。     
このSphereをつなぐようにスプラインでチューブ形状がMeshとして作成されることになります。     

![createSimpleCurve_01.jpg](./images/createSimpleCurve_01.jpg)    

また、Xformに対してマテリアルを割り当てておきます。     

Xformを選択した状態でScript Editorで「[CreateSimpleCurve.py](./CreateSimpleCurve.py)」を実行します。     

Create Curveウィンドウが表示されました。     
![createSimpleCurve_02.png](./images/createSimpleCurve_02.png)    

"Number of divisions"で分割数を指定して"Create"ボタンを押します。     
Sphereを曲線上でつないだチューブ形状がMeshとして生成されます。     
![createSimpleCurve_03.png](./images/createSimpleCurve_03.png)    
![createSimpleCurve_04.png](./images/createSimpleCurve_04.png)    

