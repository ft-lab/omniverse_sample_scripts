# extension.tomlでの記述内容

"extension.toml"に記載する内容の覚書です。     

## 他のExtensionを使用し、機能を呼び出したい

他のExtensionの機能を使用したい場合、[dependencies]にExtension名を追加します。     

```
[dependencies]
"omni.audioplayer" = {}
```
この場合は「omni.audioplayer」を有効にします。      
こうすることで、Pythonで「import omni.audioplayer」が使用できるようになります。

なお、参照で記載するExtension名は [[python.module]] に記載しているものと同じになります。     
以下は「omni.audioplayer」内の"extension.toml"の記載です。     
```
[[python.module]]
name = "omni.audioplayer"
```
ここで記載しているExtensionがOnになっていない場合は、対象のExtensionを起動した時に自動的にOnになります。     

## 外部のC/C++モジュールを呼び出す

Windows環境の場合、dllの形で外部関数を作成します。    
これをExtensionから呼び出すことができます。      

```
[[native.library]]
path = "bin/win/x64/OmniverseSimpleDLL.dll"
```

DLL呼び出しのサンプルExtensionは「[ft_lab.sample.callDLL](../ft_lab.sample.callDLL)」をご参照くださいませ。     
