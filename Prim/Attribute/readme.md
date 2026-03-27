# Attribute

|検証|Omniverse Kit|OpenUSD|  
|---|---|---|   
|OK|v.110.0.0|v.25.11|  

プリム上のカスタム属性（attribute / primvar）を操作するサンプル集です。

## 使い方

- スクリプトエディタで対象プリムを選択してから実行してください。選択がない場合は `/World` を対象にします。

## ファイル一覧

| ファイル | 説明 |
|---|---|
| [create_attribute.py](./create_attribute.py) | 属性を作成しデフォルト値をセットします。 |
| [get_attribute_value.py](./get_attribute_value.py) | 指定属性の値を取得します（存在チェックあり）。 |
| [set_attribute_value.py](./set_attribute_value.py) | 指定属性に値を設定します（存在しない場合は作成）。 |
| [delete_attribute.py](./delete_attribute.py) | 指定属性を安全に削除します（存在確認→削除）。 |
| [list_attributes.py](./list_attributes.py) | プリム上の属性一覧（名前・型）を表示します。 |

