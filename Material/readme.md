# Material

マテリアルの割り当て/取得。     
なお、テクスチャファイルについては「[textures](./textures)」をローカルの相対パスの位置に配置してご使用くださいませ。    

マテリアルは UsdShade.Material ( https://graphics.pixar.com/usd/release/api/class_usd_shade_material.html )で定義されます。     

Primに対して以下のようにバインドすることで、対象形状にマテリアルが反映されます。    
```python
UsdShade.MaterialBindingAPI(prim).Bind(material)
```
また、マテリアルはShaderを割り当てる必要があります。    
UsdShade.Shader ( https://graphics.pixar.com/usd/release/api/class_usd_shade_shader.html )。     
このShaderは、USD標準のUsdPreviewSurfaceを使用するほか、独自のShaderを割り当てることができます。    
Omniverseの場合は、MDL ( https://www.nvidia.com/ja-jp/design-visualization/technologies/material-definition-language/ )としてマテリアルを表現します。     

|サンプル|説明|     
|---|---|     
|[GetMaterial](./GetMaterial)|マテリアルを取得 
|[UsdPreviewSurface](./UsdPreviewSurface)|マテリアルの割り当て (UsdPreviewSurface)|     
|[OmniPBR](./OmniPBR)|マテリアルの割り当て (OmniPBR)|     
