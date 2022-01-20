# Extension

簡単なサンプルのExtensionです。      
Extensionはモジュール的にOmniverse(Kit)を使ったアプリを拡張します。      
ExtensionはベースはPythonとして記載し、別途C言語(動的ライブラリとして関数呼び出し)で外部機能を実装することができます。      

## サンプルExtension

|Extension|説明|     
|---|---|     
|[ft_lab.sample.hello](./ft_lab.sample.hello/readme.md)|開始(startup)/破棄(shutdown)のみの簡単なExtension|     
|[ft_lab.sample.callDLL](./ft_lab.sample.callDLL/readme.md)|C言語のDLLより関数を読み込む|     

