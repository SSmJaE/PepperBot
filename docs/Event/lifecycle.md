## before
return False

set context['xxxx']

## 事件响应
可以在事件响应和after中接受到，向后传播

## after
当接收到对应的消息的“副作用”时，这个应该是针对于bot，chain等的实例方法的，如group_msg, kickout
is coruuteine
is normal function


> 通过flag实现
可以手动实现

if sender.userId == bot.userId:
    if len(sendedMessage) == len(newMessage):

        isSameMessageFlag = True
        for index, segment in enumerate(sendedMessage):
            if segment != newMessage[index]:
                isSameMessageFlag = False

        if isSameMessageFlag:
            # 此时可以确定是同一条消息
            pass
