# Geometry

ジオメトリを作成するためのサンプルです。     

## primvarの仕様変更

USD 20.08からUSD 22.11にかけて、primvarの仕様が変更されました。     
「[UsdGeom.PrimvarsAPI](https://openusd.org/release/api/class_usd_geom_primvars_a_p_i.html)」を使用してprimvarを操作する必要があります。    
     
## Samples

|サンプル|説明|     
|---|---|     
|[CreateSphere](./CreateSphere)|球を作成<br>UsdGeom.Sphere ( https://graphics.pixar.com/usd/release/api/class_usd_geom_sphere.html )を使用。|    
|[CreateCube](./CreateCube)|直方体を作成<br>UsdGeom.Cube ( https://graphics.pixar.com/usd/release/api/class_usd_geom_cube.html )を使用。|    
|[CreateMesh](./CreateMesh)|Meshを作成/Mesh情報を取得<br>UsdGeom.Mesh ( https://graphics.pixar.com/usd/release/api/class_usd_geom_mesh.html )を使用。|    

|ファイル|説明|     
|---|---|     
|[GetMeshPrimvars.py](./GetMeshPrimvars.py)|選択Meshの「primvars:xxx」の情報を取得。|    
|[SetMeshPrimvars.py](./SetMeshPrimvars.py)|選択Meshにprimvarを追加/削除。|    


