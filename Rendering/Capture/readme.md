# Capture

レンダリング画像を取得。     
Kit.104で動作するように確認。     

"omni.kit.viewport.utility"を使用したキャプチャ。      

|サンプル|説明|     
|---|---|     
|[CaptureRenderingColorToFile.py](./CaptureRenderingColorToFile.py) |レンダリング画像をファイルに保存。|     
|[CaptureRenderingColorToBuffer.py](./CaptureRenderingColorToBuffer.py) |レンダリング画像をバッファ(RGBA)で取得し、PILのImageで表示。|     
|[CaptureCameraRenderingColorToBuffer.py](./CaptureCameraRenderingColorToBuffer.py) |指定のカメラからのレンダリングを行い、PILのImageで表示。<br>レンダリングのViewportは非表示にして、オフラインレンダリングを行う。|     

## 古い実装

キャプチャを行うには、Extensionの"omni.syntheticdata"をOnにして使用する必要があります。     

|サンプル|説明|     
|---|---|     
|[CaptureRenderingDepth.py](./CaptureRenderingDepth.py)|Synthetic Data Sensorを使用して、レンダリングのDepthをファイル保存。<br>また、Viewportで"Synthetic Data Sensor"の"Depth"をOnにしておく必要があります。<br>![capture_SyntheticDataSensor_1.jpg](./images/capture_SyntheticDataSensor_1.jpg)|     



