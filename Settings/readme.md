# Settings

carb.settingsより、設定を取得します。     
これは"/kit/config/kit-core.json"の情報を読み取ります。     


|ファイル|説明|     
|---|---|     
|[GetKitVersion.py](./GetKitVersion.py)|Omniverse Kitのバージョンを取得|     
|[GetRenderingSize.py](./GetRenderingSize.py)|レンダリングサイズを取得|     
|[GetRenderMode.py](./GetRenderMode.py)|Render Mode(RTX Real-time/RTX Path-traced)を取得、設定<br>Render Modeは、コルーチン内で「await omni.kit.app.get_app().next_update_async()」で1フレーム待ってから変更したほうが安全。|     

