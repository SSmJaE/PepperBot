---
title: 初始化项目
---



:::warning
该功能尚未实现
:::

可以使用cli命令来初始化项目

```bash
pepperbot init --name=hello_world  --template=default
```

```bash
- hello_world
    - src
        - commands
            - __init__.py
            - example_command.py
        - handlers
            - __init__.py
            - example_handler.py
        - main.py
    - .env
    - .gitignore
    - pyproject.toml
    - README.md
```

如果没有安装`pdm`，可以使用`pip`来安装

```bash
pip install pdm
```

然后使用`pdm`来安装依赖

```bash
pdm install
```
