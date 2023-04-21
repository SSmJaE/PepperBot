---
title: 数据库
---


`PepperBot`选择通过数据库，来实现进程间的数据共享

orm为`ormar`，基于`sqlalchemy` + `pydantic`的异步orm，支持`sqlite`、`mysql`、`postgresql`等数据库

默认使用`sqlite`，可以通过`.env`修改数据库配置

## 框架本身使用的表

## 开发者可用的表

### 实现自己的表

## 使用建议

### 在多worker中同步数据的示例
