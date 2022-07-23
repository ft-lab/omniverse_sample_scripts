# Camera

カメラ操作を行います。    
カメラはUsdGeom.Camera ( https://graphics.pixar.com/usd/release/api/class_usd_geom_camera.html ) を使用します。      

Omniverse Kit.102では「omni.kit.viewport」を使っていましたが、kit.103では「omni.kit.viewport_legacy」となりました（とりあえずの変更）。       

|ファイル|説明|     
|---|---|     
|[CreateCamera.py](./CreateCamera.py)|カメラを作成|     
|[GetCurrentCamera.py](./GetCurrentCamera.py)|カレントのカメラを情報を取得|     
|[CalcPanoramaCameraVector.py](./CalcPanoramaCameraVector.py)|立体視用の2つのカメラを作成|     
