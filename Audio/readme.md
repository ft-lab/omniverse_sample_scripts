# Audio

Audioファイルを読み込んで再生します。      
Audio自身はUSDでPrimとして指定することができます。      

UsdAudio Proposal       
https://openusd.org/release/wp_usdaudio.html

また、OmniverseでもUIとしてAudioのStageへのインポートができます。      

Audioファイルフォーマットは、wav/ogg/mp3が再生できるのを確認しています。     

USDファイルにAudioを指定でき、この場合はTimelineの指定の位置での再生が可能です。      
Pythonスクリプトから任意のタイミングでの再生するにはExtensionの`omni.audioplayer`を使用します。    

Audioファイルは [HitWall.ogg](./audio/HitWall.ogg) をサンプルとしてアップしているため、      
スクリプトから検索できる位置に配置してご利用くださいませ。      

|ファイル|説明|     
|---|---|     
|[PlaySound.py](./PlaySound.py)|Audioファイルを読み込んで再生<br>`omni.audioplayer` ExtensionをOnにする必要があります。|     

