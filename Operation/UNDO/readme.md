# UNDO

UNDO処理。    
特にSkeleton情報を変更する場合、UNDOに対応しないと正常に動作しないケースがありました。     
Omniverse Kitのドキュメントの"Bundled Extensions/omni.kit.commands"が参考になります。     

|ファイル|説明|     
|---|---|     
|[simpleClassUNDO.py](./simpleClassUNDO.py)|classを使用してUNDO対応。|     
|[CreateSphereUndo.py](./CreateSphereUndo.py)|球を生成する処理でUNDO対応して位置|     


