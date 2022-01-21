# UI

UI関連の処理を行います。     
UIは「omni.ui」からアクセスすることでさまざまなウィジットを表現できます。     
UIについては生成と破棄はセットになるためExtensionで実装するほうがよいですが、Script Editorからの実行でUI表示を行うこともできます（ただし、手動で破棄処理を呼ぶ必要あり）。     

|サンプル|説明|     
|---|---|     
|[DebugDraw](./DebugDraw/readme.md)|3Dの座標指定で、Depthによる遮蔽を考慮したラインを描画 (omni.debugdrawを使用)|     
|[DragAndDrop](./DragAndDrop/readme.md)|UIでのドラッグ＆ドロップ|     
|[DrawImage](./DrawImage/readme.md)|スクリーンにイメージをオーバーレイして描画|     
|[Viewport](./Viewport/readme.md)|ビューポートにオーバレイして表示|     
|[Window](./Window/readme.md)|新しいウィンドウを表示|     
