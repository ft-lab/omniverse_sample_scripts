# Transform

Transform(scale/rotate/translate)情報の取得/設定。    

|ファイル|説明|    
|---|---|    
|[GetTransform.py](./GetTransform.py)|選択された形状のTransform要素を取得|    
|[GetTransformOrder.py](./GetTransformOrder.py)|選択された形状のxformOpOrder(Transformの変換順)を取得|    
|[SetTransform.py](./SetTransform.py)|Cubeを作成し、Transformを指定|    
|[GetWorldTransform.py](./GetWorldTransform.py)|選択形状のTransformをワールド変換して表示|    
|[GetLocalMatrix.py](./GetLocalMatrix.py)|選択形状のローカル座標での4x4変換行列を取得|    
|[GetTransformVectors.py](./GetTransformVectors.py)|UsdGeom.XformCommonAPIを使用して、選択形状の移動/回転/スケール/Pivot/回転を取得|    
|[SetTranslate.py](./SetTranslate.py)|選択形状の移動を指定。存在しなければxformOpOrderも考慮して追加|    
|[SetScale.py](./SetScale.py)|選択形状のスケールを指定。存在しなければxformOpOrderも考慮して追加|    
|[SetRotate.py](./SetRotate.py)|選択形状の回転を指定。存在しなければxformOpOrderも考慮して追加|
|[SetPivot.py](./SetPivot.py)|選択形状のPivotを指定。存在しなければxformOpOrderも考慮して追加|
