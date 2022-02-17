# Viewport

ビューポート上のオーバレイ表示。    

## ビューポートの位置とサイズ

以下のように実行すると、ビューポートの矩形情報を取得できます。     
```python
import omni.kit

viewportI = omni.kit.viewport.acquire_viewport_interface()
vWindow = viewportI.get_viewport_window(None)

vwRec = vWindow.get_viewport_rect()
```
このときの「vwRec」をビューポートの矩形とします。    
メインメニューの左上を(0, 0)として原点とし、相対位置として
(vwRec[0], vwRec[1]) - (vwRec[2], vwRec[3]) がビューポートの左上と右下の座標となります。      
![viewport_rect.jpg](./images/viewport_rect.jpg)      


## サンプル

|ファイル|説明|     
|---|---|     
|[DrawText.py](./DrawText.py)|ビューポートにテキストを描画<br>![DisplayText.png](./images/DisplayText.png)|     
|[DrawText2.py](./DrawText2.py)|ビューポートに複数行のテキストを描画<br>![DisplayText2.png](./images/DisplayText2.png)|     
|[DrawRandomRect.py](./DrawRandomRect.py)|ビューポートにランダムに小さい矩形を描画<br>![DrawRandomRect.png](./images/DrawRandomRect.png)|     
|[UpdateText.py](./UpdateText.py)|ビューポートに10秒間カウントアップするテキストを描画。<br>asyncio.ensure_future()でタスクを起動。<br>await asyncio.sleep(1) で待つ<br>![UpdateText.png](./images/UpdateText.png)|     
|[UpdateText2.py](./UpdateText2.py)|ビューポートにカウントアップするテキストを描画。<br>time.time()で1秒の間隔ごとに更新。<br>![UpdateText2.png](./images/UpdateText2.png)|     
|[GetViewportRect.py](./GetViewportRect.py)|ビューポートの矩形情報を取得|     
|[DrawPrimName.py](./DrawPrimName.py)|選択形状の中央にPrim名を表示。<br>選択されたPrimのワールドポジションをスクリーン座標に変換。<br>ビューポート上の座標に変換して"omni.ui.Label"でテキストを描画しています。<br>![DrawPrimName.png](./images/DrawPrimName.png)|     

