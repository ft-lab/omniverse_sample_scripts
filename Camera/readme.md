# Camera

カメラ操作を行います。    
カメラはUsdGeom.Camera ( https://graphics.pixar.com/usd/release/api/class_usd_geom_camera.html ) を使用します。      

Omniverse Kit.102では「omni.kit.viewport」を使っていましたが、kit.103では「omni.kit.viewport_legacy」となりました（とりあえずの変更）。       

kit.104では「omni.kit.viewport_legacy」は廃止になっています。      
```python
import omni.kit.viewport.utility

# Get active viewport window.
active_vp_window = omni.kit.viewport.utility.get_active_viewport_window()
viewport_api = active_vp_window.viewport_api

# Get camera path ("/OmniverseKit_Persp" etc).
cameraPath = viewport_api.camera_path.pathString
```
としてviewport_apiからカメラのPrimパスを取得します。      
kit.104は"Viewport 2.0"となっており、複数のViewportを持つことができます。     
そのため、アクティブなビューポートを"omni.kit.viewport.utility.get_active_viewport_window()"から取得してきています。      


## サンプル

|ファイル|説明|     
|---|---|     
|[CreateCamera.py](./CreateCamera.py)|カメラを作成|     
|[GetCurrentCamera.py](./GetCurrentCamera.py)|カレントのカメラを情報を取得|     
|[CalcPanoramaCameraVector.py](./CalcPanoramaCameraVector.py)|立体視用の2つのカメラを作成|     
