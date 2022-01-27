# Prim

USDのPrim(ノード相当)を操作します。     

|ファイル|説明|     
|---|---|     
|[IsValid.py](./IsValid.py)|指定のパスのPrimが存在するかチェック(IsValid)|     
|[GetPrimNamePath.py](./GetPrimNamePath.py)|指定のPrimの名前とパスを取得|     
|[GetDefaultPrim.py](./GetDefaultPrim.py)|StageのルートとなるPrim(DefaultPrim)を取得|     
|[CreateXform.py](./CreateXform.py)|空のノード（Nullノード相当）を作成。<br>USDではこれを"Xform"と呼んでいます。<br>UsdGeom.Xform ( https://graphics.pixar.com/usd/release/api/class_usd_geom_xform.html )を使用します。|     

|サンプル|説明|     
|---|---|     
|[Visibility](./Visibility)|Primの表示/非表示|    
|[Kind](./Kind)|PrimのKindを取得/設定|    
|[Transform](./Transform)|Transform(scale/rotate/translate)の取得/設定|    
|[TypeName](./TypeName)|PrimのTypeName(Xform/Mesh/DistantLightなど)を取得|    
|[Skeleton](./Skeleton)|Skeletonでの情報を取得|    
|[Reference](./Reference)|参照(Reference)を使った複製|    
|[PointInstancer](./PointInstancer)|アセット(USDで指定)を複数の位置/回転/スケールで複製配置(PointInstancer)|    

