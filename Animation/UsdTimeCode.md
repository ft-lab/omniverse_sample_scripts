# Usd.TimeCode(value)とUsd.TimeCode.Default()の違い

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


