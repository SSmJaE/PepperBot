## 注册事件

在adapter中，定义事件属于 meta common group private channel的哪种

## 注册指令触发

如果是消息类型的事件，将事件注册入`COMMAND_TRIGGER`

## 注册参数

在adapter对应的kwargs中，为该事件配置可用参数

`EventHandlerKwarg`的value，如果是函数，可接受的参数，在`core.event.handle`中的`get_kwargs`中定义
有
        protocol=protocol,
        mode=mode,
        raw_event=raw_event,
        source_id=source_id,
        bot=bot_instance,
    这五个
