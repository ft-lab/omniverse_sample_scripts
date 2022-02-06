# UnitsToCentimeters

Stageの単位をセンチメートルに統一します。     
[UnitsToCentimeters.py](./UnitsToCentimeters.py) は、
metersPerUnitを0.01に変換するスクリプトです。     

## 使い方

このスクリプトは、StageのmetersPerUnitが0.01（センチメートル）でない場合に
DefaultPrimのscaleを調整し、metersPerUnitを0.01に置き換えます。     
ルートPrimがXformで「DefaultPrim」の指定がされているのが必要条件になります。    

なお、Nucleus上のusdファイルの場合はmetersPerUnitの変更が許可されないことがありました。    
そのため、このスクリプトはローカルのusdに対して行うようにしてください。      

なお、このスクリプトはファイル保存は行いません。    
必要であれば、処理後にusdファイルを保存してご使用くださいませ。    

