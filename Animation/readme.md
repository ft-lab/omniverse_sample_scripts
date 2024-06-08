# Animation

アニメーション関連の処理を行います。      

USDのアニメーションは、それぞれの要素にキーフレームを登録することでタイムラインに沿った動きを与えます。     
アニメーションを割り当てることができる要素は以下のようなものがあります。     

* Transform : Primごとの変換のTralslate, Rotate, Scale
* Skeleton
  * ボーン (USDではJoint)ごとのTralslate, Rotate, Scale
  * BlendShape

Skeletonを使う場合は、Meshに対してスキンを割り当てます。スキンはJointとMeshの頂点をつなぐ役割をします。     
BlendShapeはMeshの頂点をグループ化し複数の移動量を持つShape Keyを与えます。    
このキーをモーション時にスムーズに変形させることにより動きを表現します。    
BlendShapeは人の顔の表情のような、ボーンでの変形が難しい動きに向いています。     

|ファイル|説明|     
|---|---|     
|[GetTimeCode.py](./GetTimeCode.py)|現在のStageの開始/終了TimeCode、TimeCodesPerSecond(フレームレート)を取得。|     
|[GetCurrentTimeCode.py](./GetCurrentTimeCode.py)|現在のタイムコード（フレーム位置）を取得。|     
|[TransformAnimation.py](./TransformAnimation.py)|Translate, Rotate, Scaleのキーフレーム指定|     
|[SkeletonSkin.py](./SkeletonSkin.py)|MeshへのSkeleton、Skinの割り当て|     

## Usd.TimeCode(value)とUsd.TimeCode.Default()の違い

キーフレームを割り当てる場合は以下のように指定します。  

```python
primPath = "/World/sphere"
prim = createSphere(primPath, 20.0)

# Set Keyframe.
xformAPI = UsdGeom.XformCommonAPI(prim)
xformAPI.SetTranslate(Gf.Vec3d(0, 0, 0), Usd.TimeCode(0))
xformAPI.SetTranslate(Gf.Vec3d(0, 100, 0), Usd.TimeCode(50))
```
SetTranslateの第二引数がキーフレーム位置となります。  

この場合、usdaファイルでは以下のようになっています。  
```
double3[] xformOp:translate.timeSamples = {
    0: [(0, 0, 0)],
    50: [(0, 100, 0)],
}
```
"xformOp:translate.timeSamples"となっています。  

一方、このUsd.TimeCode(v)を省略した場合は **Usd.TimeCode.Default()** が指定されたことになります。  

```python
xformAPI.SetTranslate(Gf.Vec3d(0, 0, 0))
```
もしくは、  
```python
xformAPI.SetTranslate(Gf.Vec3d(0, 0, 0), Usd.TimeCode.Default())
```

この場合、usdaファイルでは以下のようになっています。  
```
  double3 xformOp:translate = (0, 0, 0)
```
"xformOp:translate"となっています。  
この"TimeCode.Default()"を使用した場合は対象primそのものが持つtransform要素の指定になります(アニメーションをPlayしないときの姿勢)。  


