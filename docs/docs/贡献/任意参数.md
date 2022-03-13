## 如何实现任意参数

这一部分涉及技术细节，完全可以跳过，如果你对实现任意参数比较感兴趣，可以看一下这部分

通过 inspect 包，以及**annotation**，**code**等 dunder，我们可以获取到方法/函数定义的参数，以及他们的类型

```py3
[args, varargs, varkw] = inspect.getargs(method.__code__)
```

因此我们可以通过参数名，判断具体定义了哪些参数，按需传入

参数的动态传入，可以查看[fit_kwargs 函数](https://github.com/SSmJaE/PepperBot/blob/master/pepperbot/utils/common.py)

通过参数的类型，我们甚至可以判断参数的类型是否合法/有效，将问题在初始化解决扼杀

参数类型的检测，可以查看[cache 函数](https://github.com/SSmJaE/PepperBot/blob/master/pepperbot/parse/cache.py)

## 可以使用的参数

根据我们在事件响应中提到的，我们可以通过事件名来定义事件回调，那么每个事件回调可用的参数有哪些呢？

[这份文件](https://github.com/SSmJaE/PepperBot/blob/master/pepperbot/parse/kwargs.py#L62)列举了事件名和其对应的参数，以及该参数的类型，接下来我们通过实例说明如何使用

其中 key 为事件名，value 为参数列表

注意，所有事件都有一个 event 参数，类型是 Dict 或者 Dict[str, Any]，event 参数是一个字典，保存了当前的原始事件，

因为所有事件响应中，这个参数的名称和类型都完全一致，所以没有在这里列出，而是之后一起注入的
