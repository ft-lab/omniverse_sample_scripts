# Viewport

ビューポート上のオーバレイ表示。    
ビューポートの特定位置に2D図形の描画やテキスト描画、3Dのワイヤーフレーム描画などを行います。      
Omniverse Kit.102/103/104で仕様が変わっており、ここではKit.104に沿うようにしています。      

参考 :      
https://docs.omniverse.nvidia.com/kit/docs/omni.kit.viewport.docs/latest/index.html     


## ビューポートは複数持つことができる

Kit.103以降では、複数のビューポートを持てるようになりました（ただし、複数のビューポートは同じレンダラの種類になる）。     
![viewport_104_01](./images/viewport_104_01.jpg)     
クリックして選択したビューポートがアクティブなビューポートとなります。     

以下で、現在のアクティブなビューポートの"viewport_api"を取得できます。     
このクラスからビューポート情報の取得を行うことになります。     
```python
import omni.kit

active_vp_window = omni.kit.viewport.utility.get_active_viewport_window()
viewport_api = active_vp_window.viewport_api
```

## 取得できるビューポート情報

「[GetActiveViewportInfo.py](GetActiveViewportInfo.py)」にサンプルを上げています。      
以下のような要素をViewport APIから取得できます。     

* カメラのPrim Path ("/OmniverseKit_Persp"など)
* レンダリングの解像度
* ビューポートで使用しているStage
* Projection/Transform/View Matrix

```python
# Get camera path ("/OmniverseKit_Persp" etc).
cameraPath = viewport_api.camera_path.pathString
print("cameraPath : " + cameraPath)

# Resolution.
resolution = viewport_api.resolution
print("Resolution : " + str(resolution[0]) + " x " + str(resolution[1]))

# Stage (Usd.Stage).
print(viewport_api.stage)

# Projection matrix (Gf.Matrix4d).
print(viewport_api.projection)

# Transform matrix (Gf.Matrix4d).
print(viewport_api.transform)

# View matrix (Gf.Matrix4d).
print(viewport_api.view)
```

Viewport APIは以下に詳しい使用例が記載されているので参考になります。     
https://docs.omniverse.nvidia.com/kit/docs/omni.kit.viewport.docs/latest/viewport_api.html     

## ワールド座標からスクリーン座標への変換 (Space Mapping)

「[WorldToScreen.py](WorldToScreen.py)」にサンプルを上げています。      
上記以外の機能として、ワールド座標上の位置をスクリーンの2D座標に変換してくることができます(この逆も可能)。     
これと"omni.ui.scene"を使うことで、ビューポートへのオーバーレイ描画を容易に行うことができます。      

```python

# World to NDC space (X : -1.0 to +1.0, Y : -1.0 to +1.0).
p = (0, 0, 0)
p_screen = viewport_api.world_to_ndc.Transform(p)

# NDC to Pixel space.
sPos, in_viewport = viewport_api.map_ndc_to_texture_pixel(p_screen)
if in_viewport:
    print(sPos)
```

### NDC space

"NDC space"は、ビューポート全体をX方向に-1.0から+1.0、Y方向に-1.0から+1.0としたときの座標系です。      
![viewport_104_02](./images/viewport_104_02.jpg)     

### Pixel space

"Pixel space"は、ビューポートのレンダリング画像内のピクセル座標です。    
これはViewport APIの"resolution"で取得できる解像度の範囲のピクセル位置を表します。     
以下は解像度が1280 x 720ピクセルの場合のPixel spaceの例です。     
![viewport_104_03](./images/viewport_104_03.jpg)     

## キャプチャ

その他、レンダリング画像のキャプチャ機能があります。     
※ まだ未記載。     

## サンプル

|ファイル|説明|     
|---|---|     
|[DrawText.py](./DrawText.py)|ビューポートにテキストを描画<br>![DisplayText.png](./images/DisplayText.png)|     
|[DrawText2.py](./DrawText2.py)|ビューポートに複数行のテキストを描画<br>![DisplayText2.png](./images/DisplayText2.png)|     
|[DrawRandomRect.py](./DrawRandomRect.py)|ビューポートにランダムに小さい矩形を描画<br>![DrawRandomRect.png](./images/DrawRandomRect.png)|     
|[UpdateText.py](./UpdateText.py)|ビューポートに10秒間カウントアップするテキストを描画。<br>asyncio.ensure_future()でタスクを起動。<br>await asyncio.sleep(1) で待つ<br>![UpdateText.png](./images/UpdateText.png)|     
|[UpdateText2.py](./UpdateText2.py)|ビューポートにカウントアップするテキストを描画。<br>time.time()で1秒の間隔ごとに更新。<br>![UpdateText2.png](./images/UpdateText2.png)|     
|[UpdateDrawImage.py](./UpdateDrawImage.py)|"omni.ui.ImageWithProvider"を使用して、ファイルから読み込んだ画像をビューポートに表示します。<br>"omni.kit.app.get_app().get_update_event_stream().create_subscription_to_pop"使用時は omni.ui.Imageでの描画がうまく反映されないようなのでそれの変わりです。|   
|[GetViewportRect.py](./GetViewportRect.py)|ビューポートの矩形情報を取得|     
|[GetActiveViewportInfo.py](./GetActiveViewportInfo.py)|アクティブなビューポートの情報を取得(omni.kit Viewport API)|     
|[WorldToScreen.py](./WorldToScreen.py)|ワールド座標位置からスクリーン上の位置に変換(omni.kit Viewport API)|     


