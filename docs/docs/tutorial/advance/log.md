---
title: 日志
---


## PepperBot中的日志

PepperBot的日志是基于`loguru`的再封装

```py
from pepperbot import logger

logger.info("")
logger.debug("")
```

配合配置文件，调整日志的显示等级，可以实现非常灵活的控制

## 日志的显示等级

|Level | 对应的值 | 调用方法 |
|:----:|:-------:|:-------:|
|TRACE | 5 | logger.trace() |
|DEBUG | 10 | logger.debug() |
|INFO | 20 | logger.info() |
|SUCCESS | 25 | logger.success() |
|WARNING | 30 | logger.warning() |
|ERROR | 40 | logger.error() |
|CRITICAL | 50 | logger.critical() |

默认为`INFO`(20)，即只显示`INFO`、`SUCCESS`、`WARNING`、`ERROR`、`CRITICAL`等级的日志

具体如何修改，可以参考[配置文件](./config.md)

## 输出日志至文件
