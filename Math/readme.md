# Math

ベクトルや行列計算関連。     
USDのベクトル/行列計算は、"Gf"にまとまっているためそれを使用します。      
numpyを経由しなくても計算できます。     

ベクトルはfloat型のGf.Vec3f ( https://graphics.pixar.com/usd/release/api/class_gf_vec3f.html )、
double型のGf.Vec3d ( https://graphics.pixar.com/usd/release/api/class_gf_vec3d.html )が使用されます。    

行列はfloat型のGf.Matrix4f ( https://graphics.pixar.com/usd/release/api/class_gf_matrix4f.html )、
double型のGf.Matrix4d ( https://graphics.pixar.com/usd/release/api/class_gf_matrix4d.html )が使用されます。    


|ファイル|説明|     
|---|---|     
|[CalcDotCrossProduct.py](./CalcDotCrossProduct.py)|ベクトルの内積/外積計算|     
|[CalcMatrix.py](./CalcMatrix.py)|4x4行列の計算。行列とベクトルの乗算|     
|[CalcVector3.py](./CalcVector3.py)|Vector3の計算.|     
|[DecomposeTransform.py](./DecomposeTransform.py)|行列を移動(translate), 回転(rotation), スケール(scale)に変換|     
|[GetVector3Length.py](./GetVector3Length.py)|Vector3の長さを計算|     
|[VectorToRotationAngle.py](./VectorToRotationAngle.py)|指定のベクトルをXYZ軸回転の角度（度数）に変換|     
|[NormalizeVector3.py](./NormalizeVector3.py)|Vector3の正規化|     
|[QuatToRotation.py](./QuatToRotation.py)|クォータニオンと回転角度（度数）の変換|     
|[TransRotationFrom2Vec.py](./TransRotationFrom2Vec.py)|ベクトルAをベクトルBに変換する回転を計算。|     


