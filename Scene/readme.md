# Scene

シーン(Stage)の情報を取得/操作します。     

|ファイル|説明|     
|---|---|     
|[StageUpAxis.py](./StageUpAxis.py)|Stageのアップベクトルの取得/設定|     
|[CreateHierarchy.py](./CreateHierarchy.py)|Xformを使って階層構造を作って形状を配置<br>![createHierarchy_img.jpg](./images/createHierarchy_img.jpg)|     
|[GetAllFacesCount.py](./GetAllFacesCount.py)|シーン内のすべてのMeshの面数を合計して表示。<br>対象はMesh/PointInstancer。|     
|[TraverseHierarchy.py](./TraverseHierarchy.py)|シーンの階層構造をたどってPrim名を表示。<br>Meshの場合はMeshの面数も表示。|     
|[Traverse_mesh.py](./Traverse_mesh.py)|Usd.PrimRangeを使ってPrimを取得し、Meshのみを格納|     
|[GetMetersPerUnit.py](./GetMetersPerUnit.py)|metersPerUnitの取得/設定|     
|[NewStage.py](./NewStage.py)|何も配置されていない新しいStageを作成します。<br>なお、直前のStageの変更は保存されません。|     
|[CloseStage.py](./CloseStage.py)|現在のStageを閉じます。<br>なお、直前のStageの変更は保存されません。|     
|[OpenUSDFile.py](./OpenUSDFile.py)|指定のUSDファイルを開きます。<br>なお、直前のStageの変更は保存されません。|     

## レイヤ関連

|ファイル|説明|     
|---|---|     
|[GetRealPath.py](./Layers/GetRealPath.py)|読み込んだStageのパスを取得|     
|[GetSublayers.py](./Layers/GetSublayers.py)|SubLayerのパスを取得|     