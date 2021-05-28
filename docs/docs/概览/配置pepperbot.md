:::info
需要python 3.8及以上版本
:::
## 安装

### 稳定版本
> PepperBot使用Poetry管理依赖，建议使用Poetry进行开发


#### 使用poetry
```
pip install poetry
poetry add pepperbot
```

#### 使用pip
```
pip install pepperbot
```

### 最新版本
```
git clone https://github.com/SSmJaE/PepperBot.git
pip install poetry
poetry install
```



## 使用
- 目前建议直接修改demo
- PepperBot的端口，需要和go-cqhttp中设置的一致
```py
# demo文件最下方
if __name__ == "__main__":
    run(debug=True, port=53521)
```
- 开启debug，修改demo文件(及demo文件中导入的文件)时，PepperBot将会自动重启服务

## 运行
### 使用poetry
```
poetry run python ./demos/1.py
```
### 使用python
```
python ./demos/1.py
```

:::warning
需要同时运行go-cqhttp和PepperBot

简单来说，就是打开两个窗口，一个运行go-cqhttp，一个运行PepperBot
:::