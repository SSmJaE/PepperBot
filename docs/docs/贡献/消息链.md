在`core.message.construct_chain`中，构造消息链对象

当接收到事件时，使用`segment_factory`将各个协议的事件，转换为统一的chain

QQ的消息链有多个segment，微信和Telegram都只有一个

identifier用于辨别两个segment是否相等

当通过api，将chain发送至各个协议端时，使用每个`segment`对象对应的`to_[protocol]`方法，转换为该api调用所需要的数据格式

如果消息链有多个segment，qq可以一次发送，微信需要多次调用api

telegram暂时多次调用api，可以转换成html，实现图文混排
