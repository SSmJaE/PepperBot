---
title: 配置文件
---

## 配置环境变量

PepperBot的环境变量管理，基于Pydantic的[BaseSettings](https://pydantic-docs.helpmanual.io/usage/settings/)

PepperBot中，我们约定

- `.env`文件需要放置在根目录
- 所有的配置项，都以`p_`开头
- 嵌套的配置项，统一使用json格式

比如，我们想要配置日志的等级，从默认的`INFO`修改为`DEBUG`

那么，我们只需要在根目录建立一个名为`.env`的文件，然后在其中输入如下配置

```ini
p_logger={"level":10}
```

具体可以修改哪些日志项，分别有什么功能，可以在项目根目录下的config.py文件中查看

TODO : 将config中的配置项，输出为格式友好的表格
