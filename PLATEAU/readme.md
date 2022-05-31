# PLATEAU

Project PLATEAU ( https://www.mlit.go.jp/plateau/ )の都市データをOmniverseにインポートします。      

G空間情報センターの「3D都市モデルポータルサイト」( https://www.geospatial.jp/ckan/dataset/plateau )の「東京都23区」より、     
OBJ形式のデータを使用しています。      

また、地形のテクスチャについてはGeoTIFFを分割して使用しました。     

## 使い方

### 東京23区の地形と建物(LOD1)を読み込み

※ テクスチャは反映しません。     

Omniverse Create 2022.1.2で確認しました。    

「3D都市モデルポータルサイト」より、「東京都23区」のobjファイル一式をダウンロードします。     
https://www.geospatial.jp/ckan/dataset/plateau-tokyo23ku/resource/9c8d65f1-a424-4189-92c0-d9e3f7c3d2db

「13100_tokyo23-ku_2020_obj_3_op.zip」がダウンロードされますので解凍します。      

Omniverse Createを起動し、新規Stageを作成します。     

「[import_PLATEAU_tokyo23ku_all_obj_lod1.py](./import_PLATEAU_tokyo23ku_all_obj_lod1.py)」の内容をScript Editorにコピーします。     

スクリプト上の in_plateau_obj_path のパス指定を、ローカルの「13100_tokyo23-ku_2020_obj_3_op.zip」を解凍したディレクトリに変更します。      

スクリプトを実行します。     
この処理は時間がかかります。数分ほど待つと、StageにPLATEAUの都市データが読み込まれます。     

以下は背景のEnvironmentを指定し、RTX-Interactive (Path Tracing)にしています。     
![plateau_01_01.jpg](./images/plateau_01_01.jpg)     
![plateau_01_02.jpg](./images/plateau_01_02.jpg)    

このLOD1のみの都市データは、Omniverse Createで約15GBくらいのメモリを消費します。      
OSのメモリは32GBあれば足ります。     

### 東京23区の地形と建物(LOD1)を読み込み + 地形のテクスチャを反映


## ファイル

|ファイル|説明|     
|---|---|     
|[import_PLATEAU_tokyo23ku_all_obj_lod1.py](./import_PLATEAU_tokyo23ku_all_obj_lod1.py)|東京23区のPLATEAUのobjファイルより、LOD1の都市モデルをOmniverseにインポートします。<br>dem/bldg(LOD1)を読み込み。<br>テクスチャは反映していません。|
|[divide_GeoTiff_images.py](./divide_GeoTiff_images.py)|東京23区のPLATEAUのGeoTIFFファイルを10x10分割して、jpeg形式で指定のフォルダに出力します。|



