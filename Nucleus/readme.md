# Nucleus

OmniverseではUSDからの保存はNucleusの指定のパス(omniverse://localhost/xxx/yyy.usd)に出力できます。    
別途、Nucleus上でファイル操作を行う「omni.client」が用意されています。     


## 参考

https://docs.omniverse.nvidia.com/py/kit/source/extensions/omni.client/docs/index.html

## サンプル

|ファイル|説明|     
|---|---|     
|[existPath.py](./existPath.py)|Nucleus上のファイルまたはフォルダが存在するかチェック。|     
|[listFiles.py](./listFiles.py)|Nucleus上の指定のフォルダ内のファイルを一覧。|     
|[FileCopy.py](./FileCopy.py)|ローカルからNucleus上にファイルを転送。|     
|[createFolder.py](./createFolder.py)|Nucleus上にフォルダを作成。|     
|[deleteFile.py](./deleteFile.py)|Nucleus上のファイルやフォルダを削除。|     

