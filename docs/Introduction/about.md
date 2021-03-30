## 为什么叫PepperBot？
- 我喜欢吃农家小炒肉

## 后端
- 也就是负责与QQ通信的“无头QQ”，
- 一般建议使用go-cqhttp作为“后端”

## 业务逻辑框架
> 为什么说PepperBot是一个业务逻辑框架？
- PepperBot并没有实现与QQ通信的能力，只负责处理“业务逻辑”
- PepperBot通过与后端的通信，实现了与QQ的通信
- PepperBot基于OneBot协议，所以所有符合OneBot标准的“后端”，都可以使用

## PepperBot的命名规范及风格
> 基本符合PEP8
- 变量、参数camelCase
- 常量全大写+下划线CONSTANT_VARIABLE
- 函数，方法名全小写+下划线normal_function normal_class_method
- 类名、文件名PascalCase AClassName
- 私有变量_前缀，私有方法__前缀_privateVariable,__private_method
- 不建议使用单行if return True if a > b else False
- 不建议使用匿名函数 lambda x,y:x.a()+y.b()
- 建议使用能自说明的变量名称_privateVariable
- 节制使用列表推导、字典推导(单层可以用，多层嵌套的推导，建议展开) [a + b for a in range(20) for b in range(30) if a > 10 and b > 20]
