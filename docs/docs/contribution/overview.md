---
slug: /contribution/
---

## PepperBot 的命名规范及风格

> 基本符合 PEP8

-   变量、参数

camel_case

-   常量全大写+下划线

CONSTANT_VARIABLE

-   函数、方法名、文件名全小写+下划线

normal_function

normal_class_method

module_name

-   类名

AClassName

-   私有变量\_前缀，私有方法\_\_前缀

\_privateVariable

\_\_private_method

-   不建议使用单行 if

return True if a > b else False

-   不建议使用匿名函数

lambda x,y:x.a()+y.b()

-   建议使用能自说明的变量名称

\_privateVariable

-   节制使用列表推导、字典推导(单层可以用，多层嵌套的推导，建议展开)

[a + b for a in range(20) for b in range(30) if a > 10 and b > 20]
