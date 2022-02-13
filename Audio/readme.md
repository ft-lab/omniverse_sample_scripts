# Audio

Audioファイルを読み込んで再生します。      
Audio自身はUSDでPrimとして指定することができます。      

UsdAudio Proposal       
https://graphics.pixar.com/usd/release/wp_usdaudio.html


また、OmniverseでもUIとしてAudioのStageへのインポートができます。      

https://docs.omniverse.nvidia.com/app_create/prod_extensions/ext_audio.html

Audioファイルフォーマットは、wav/ogg/mp3が再生できるのを確認しています。     

USDファイルにAudioを指定でき、この場合はTimelineの指定の位置での再生が可能です。      
Pythonスクリプトから任意のタイミングでの再生するにはExtensionの「omni.audioplayer」を使用します。    

Audioファイルは [HitWall.ogg](./audio/HitWall.ogg) をサンプルとしてアップしているため、      
スクリプトから検索できる位置に配置してご利用くださいませ。      

|ファイル|説明|     
|---|---|     
|[PlaySound.py](./PlaySound.py)|Audioファイルを読み込んで再生<br>"omni.audioplayer" ExtensionをOnにする必要があります。|     

