# Extension

簡単なサンプルのExtensionです。      
Extensionはモジュール的にOmniverse(Kit)を使ったアプリを拡張します。      
ExtensionはベースはPythonとして記載し、別途C言語(動的ライブラリとして関数呼び出し)で外部機能を実装することができます。      

## Extensionの詳しいドキュメント

Extensionは構成のルールがあります。      
Omniverse Createの[Help]-[Developers Manual]からOmniverse Kitのドキュメントの「Extensions」で詳しく解説されています。    

## サンプル

|Extension|説明|     
|---|---|     
|[ft_lab.sample.hello](./ft_lab.sample.hello)|開始(startup)/破棄(shutdown)のみの簡単なExtension|     
|[ft_lab.sample.callDLL](./ft_lab.sample.callDLL)|C言語のDLLより関数を読み込む|     
|[ft_lab.sample.menu](./ft_lab.sample.menu)|メニューを追加。<br>![extension_menu_01.png](./images/extension_menu_01.png)|     
|[ft_lab.sample.loadStage](./ft_lab.sample.loadStage)|Extension内に配置したusdファイルを新規Stageとして読み込む|     

