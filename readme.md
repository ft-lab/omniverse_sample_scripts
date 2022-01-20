# Omniverse sample scripts

NVIDIA Omniverseは、データ構造としてUSDを使用してます。     
3Dモデルやシーンのファイルへの保存、読み込みでUSDが使用されるだけでなく、    
Omniverse CreateやOmniverse MachinimaなどのOmniverseアプリ上のビュー上でもUSDを介して行われます（表示/非表示の切り替えや移動など）。      

ここでは、OmniverseアプリであるOmniverse CreateのScript Editorで試せるスクリプトのサンプルを用途別に列挙します。     
Omniverse Create 2021.3.8で確認しました。     

## はじめに

Omniverse Createで、メインメニューの [Window] - [Script Editor]を選択して、Script Editorを起動します。     

![omniverse_script_editor_01.png](./images/omniverse_script_editor_01.png)    

この中でPythonを使用してプログラムを書きます。    
左下のRunボタンを押すか、[Ctrl] +[Enter]キーを押すことで実行します。      

以下、Pythonの初歩的な説明です。     

## コメント

1行のコメントの場合、"#"から行の末尾までがコメントになります。     
```python
# comment.
```

複数行の場合は、""" から """ までがコメントになります。     
```python
"""
comment.
line2.
"""
```

## print

デバッグ用のメッセージはprintで記載します。     
```python
print('Hello Omniverse !')
```

## 機能説明用のサンプル

|サンプル|説明|     
|---|---|     
|[Camera](./Camera/readme.md)|カメラ操作|    
|[Event](./Event/readme.md)|イベント処理|    
|[Geometry](./Geometry/readme.md)|ジオメトリの作成|    
|[Material](./Material/readme.md)|マテリアルの割り当て|    
|[Math](./Math/readme.md)|ベクトル/行列計算関連|    
|[Operation](./Rendering/readme.md)|Ominverseの操作|    
|[Physics](./Physics/readme.md)|Physics(物理)処理|    
|[pip_archive](./pip_archive/readme.md)|Pythonのよく使われるモジュールの使用|    
|[Prim](./Prim/readme.md)|USDのPrim(ノード)の操作|    
|[Rendering](./Prim/readme.md)|レンダリング画像の操作|    
|[Scene](./Scene/readme.md)|シーン情報の取得|    
|[Settings](./Settings/readme.md)|設定の取得|    
|[System](./System/readme.md)|システム関連情報の取得|    
|[UI](./UI/readme.md)|UI操作|    

## ツール的なサンプル

|サンプル|説明|     
|---|---|     
|[Samples](./Samples/readme.md)|サンプルスクリプト|    

## Extension

|サンプル|説明|     
|---|---|     
|[Extensions](./Extensions/readme.md)|サンプルExtension|    
