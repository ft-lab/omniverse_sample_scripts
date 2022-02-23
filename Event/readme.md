# Event

イベント処理を行います。    

## 更新イベント

以下のように更新イベントを登録すると、コールバックとして更新処理が呼ばれます。     

```python
import omni.kit.app
import carb.events

def on_update(e: carb.events.IEvent):
    pass

subs = omni.kit.app.get_app().get_update_event_stream().create_subscription_to_pop(on_update)
```

## サンプル

|ファイル|説明|     
|---|---|     
|[UpdateInterval.py](./UpdateInterval.py)|update_event_streamの更新間隔をビューポートに表示|  

