## 2021-05-20 v0.1.0

- 事件名snake化，不camel转化了，设置事件的kwargs时更直观一点
- 包名全部小写化
- 提升commandCache为顶级，而不是GroupCache的附属，大量减少command实例的创建
- 优化项目结构，从main_entry中拆分出qq事件响应，指令响应等为独立函数，更易维护
- 自动提取as_command的参数
- 实现根据annotation自动提供参数，不再需要**kwargs了
- 支持判断Image是否是闪照的工具函数
- 规范Bot的类型，除非有特殊函数，统一使用GroupCommonBot
- 提取所有User类型至单独文件
- 可以跳过go-cqhttp缓存的事件了
- 规范化事件响应的kwargs的声明，可以方便的添加参数定义

## 2021-05-20 v0.1.1

- 发布至pypi

## 2021-05-20 v0.1.2

- 实现command的pattern装饰器，支持initial时的前缀判断

## 2022-05-03 v0.3.0

- 初步支持`Telegram`
- segment.protocol()全部异步化
- 统一所有segment在core.message.segment下，而不是在独立的adapter下
