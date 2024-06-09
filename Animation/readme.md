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

## Tips

* [Usd.TimeCode(value)とUsd.TimeCode.Default()の違い](./UsdTimeCode.md)
* [スケルトンの構造とスキン](./SkeletonSkin.md)



