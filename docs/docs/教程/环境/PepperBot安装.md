---
title: 安装
---

:::info
需要 python 3.8 及以上版本
:::

:::warning
如果你希望对接 QQ，需要同时运行 go-cqhttp 和 PepperBot

简单来说，就是打开两个窗口，一个运行 go-cqhttp，一个运行 PepperBot，微信等其他平台同理
:::

## 安装稳定版本

> PepperBot 使用 Poetry 管理依赖，建议使用 Poetry 进行开发

### 使用 poetry

```
pip install poetry
poetry add pepperbot
```

:::info
poetry第一次resolve会比较慢
:::

### 使用 pip

```
pip install pepperbot
```

## 安装最新版本

### 使用`git module`

可以使用poetry的`git module`

在`pyproject.toml`中添加

```
pepperbot = { git = "https://github.com/SSmJaE/PepperBot.git", branch = "master" }
```

这种方式比较方便，不需要手动添加`PYTHONPATH`

添加之后

```
poetry install
```

然后就像正常安装一样使用就行

### 直接clone

```
git clone https://github.com/SSmJaE/PepperBot.git
pip install poetry
poetry install
```

如果你希望在本地使用最新版本的 PepperBot，在使用 poetry 安装好 PepperBot 的依赖之后，需要手动添加`PYTHONPATH`

```
-pepperbot
    ...
    - pepperbot
    - docs
    - your_dir
        - main.py
```

将你的 bot 文件所在的根目录，放在与 docs 同级的位置

之后，你可能需要在 main.py 手动添加 import 路径，让 python 解释器知道 PepperBot 的位置

```python title="your_dir/main.py"
import sys
from os import path

BASE_DIR = path.dirname(path.dirname(path.abspath(__file__)))
sys.path.append(BASE_DIR)
```

现在，你可以在 main.py 中直接导入从 git clone 的 PepperBot 了

```py  title="your_dir/main.py"
...
sys.path.append(BASE_DIR)

from pepperbot import PepperBot
```

:::warning
注意，所有从 pepperbot 导入的语句，必须在添加路径(sys.path.append)的下方

其它模块无所谓在上还是在下
:::
