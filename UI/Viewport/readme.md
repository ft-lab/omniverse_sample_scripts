# Viewport

ビューポート上のオーバレイ表示。    

|ファイル|説明|     
|---|---|     
|[DrawText.py](./DrawText.py)|ビューポートにテキストを描画<br>![DisplayText.png](./images/DisplayText.png)|     
|[DrawText2.py](./DrawText2.py)|ビューポートに複数行のテキストを描画<br>![DisplayText2.png](./images/DisplayText2.png)|     
|[DrawRandomRect.py](./DrawRandomRect.py)|ビューポートにランダムに小さい矩形を描画<br>![DrawRandomRect.png](./images/DrawRandomRect.png)|     
|[UpdateText.py](./UpdateText.py)|ビューポートに10秒間カウントアップするテキストを描画。<br>asyncio.ensure_future()でタスクを起動。<br>await asyncio.sleep(1) で待つ<br>![UpdateText.png](./images/UpdateText.png)|     
|[UpdateText2.py](./UpdateText2.py)|ビューポートにカウントアップするテキストを描画。<br>time.time()で1秒の間隔ごとに更新。<br>![UpdateText2.png](./images/UpdateText2.png)|     
|[GetViewportRect.py](./GetViewportRect.py)|ビューポートの矩形情報を取得|     
|[DrawPrimName.py](./DrawPrimName.py)|選択形状の中央にPrim名を表示。<br>選択されたPrimのワールドポジションをスクリーン座標に変換。<br>ビューポート上の座標に変換して"omni.ui.Label"でテキストを描画しています。<br>![DrawPrimName.png](./images/DrawPrimName.png)|     

