# Prim

USDのPrim(ノード相当)を操作します。     

Primの操作は「[CommandsExecute](../Operation/CommandsExecute)」も便利に使用できます。     


|ファイル|説明|     
|---|---|     
|[IsValid.py](./IsValid.py)|指定のパスのPrimが存在するかチェック(IsValid)|     
|[GetPrimNamePath.py](./GetPrimNamePath.py)|指定のPrimの名前とパスを取得|     
|[GetDefaultPrim.py](./GetDefaultPrim.py)|StageのルートとなるPrim(DefaultPrim)を取得|     
|[SetDefaultPrim.py](./SetDefaultPrim.py)|StageのルートとなるPrim(DefaultPrim)を指定|     
|[CreateXform.py](./CreateXform.py)|空のノード（Nullノード相当）を作成。<br>USDではこれを"Xform"と呼んでいます。<br>UsdGeom.Xform ( https://graphics.pixar.com/usd/release/api/class_usd_geom_xform.html )を使用します。|     
|[CreateScope.py](./CreateScope.py)|Scopeを作成。<br>Scopeは移動/回転/スケール要素を持ちません。単純なグルーピング向けです。<br>UsdGeom.Scope ( https://graphics.pixar.com/usd/release/api/class_usd_geom_scope.html )を使用します。|     
|[GetDoubleSided.py](./GetDoubleSided.py)|ジオメトリでのDoubleSided指定の取得、設定|     
|[GetSingleSided.py](./GetSingleSided.py)|ジオメトリでのSingleSided指定の取得、設定<br>これはOmniverseでの独自の属性|     
|[GetParent.py](./GetParent.py)|選択パスの親のPrimを取得|     
|[GetChildren.py](./GetChildren.py)|選択パスの子のPrimを取得|     
|[CalcWorldBoundingBox.py](./CalcWorldBoundingBox.py)|選択形状のワールド座標でのバウンディングボックスを計算|     
|[RemovePrim.py](./RemovePrim.py)|指定のパスのPrimを削除。<br>Sdf.NamespaceEdit.Removeを使用する。|     

|サンプル|説明|     
|---|---|     
|[Visibility](./Visibility)|Primの表示/非表示|    
|[Kind](./Kind)|PrimのKindを取得/設定|    
|[Transform](./Transform)|Transform(scale/rotate/translate)の取得/設定|    
|[TypeName](./TypeName)|PrimのTypeName(Xform/Mesh/DistantLightなど)を取得|    
|[Skeleton](./Skeleton)|Skeletonでの情報を取得|    
|[Reference](./Reference)|参照(Reference)を使った複製/参照のチェック|    
|[PointInstancer](./PointInstancer)|アセット(USDで指定)を複数の位置/回転/スケールで複製配置(PointInstancer)|    
|[Variant](./Variant)|Variantを使ったPrimの切り替え|    


