## initial bot info

获取bot 元信息

### 需要修改get_bot_id

### 需要修改get_bot_instance

内部适配不同RouteMode下，返回的bot实例

## `core.event.universal`中的`registered_adapter`中添加配置

之后适配事件即可

## get_source_id

source_id是来源id，如果来自私聊，就是用户id，如果来自群聊，是群号，并不是发送这条群消息的用户的id

如果想要获取到发送这条群消息的用户的id，可以通过raw_event，

或者一般也会为该事件构造一个User或者Member参数，可以从其上获取用户id
