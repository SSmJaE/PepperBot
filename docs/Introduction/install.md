## 配置cq-gohttp
::: tip
可以参考go-cqhttp的[官方文档](https://docs.go-cqhttp.org/guide/quick_start.html#%E5%9F%BA%E7%A1%80%E6%95%99%E7%A8%8B)
:::
### 安装
- 在[go-cqhttp](https://github.com/Mrs4s/go-cqhttp/releases)的Github仓库中下载符合自己操作系统的版本

### 初始化
::: tip
可以按照自己的操作习惯，将go-cqhttp放在不同目录，不用和教程保持一致
:::
- 在项目下新建backend文件夹，将go-cqhttp的可执行文件放入其中
- 运行一次
```
cd ./backend
./go-cqhttpxxxxx.exe
```
- 第一次运行时，go-cqhttp自动生成config.hjson文件，我们需要修改配置
### 修改hjson
- 修改`uin`为自己的qq号
- 修改`password`为密码
- 修改`post_message_format`为`array`
- 修改`ws_reverse_servers`中
  - `enabled`为`true`
  - 修改`reverse_url`为`ws://127.0.0.1:端口/cqhttp/ws`
  - 端口需要和PepperBot中的端口保持一致
### 再次运行

## 配置PepperBot
> PepperBot尚未发布至pypi，目前暂时通过git获取项目代码
::: tip
需要python 3.8及以上版本
:::
### 安装

```
git clone https://github.com/SSmJaE/PepperBot.git
```
> PepperBot使用Poetry管理依赖，建议使用Poetry进行开发
#### 使用poetry
```
pip install poetry
poetry install
```
#### 使用pip
> 手动安装需要的依赖
> 
> 暂时未提供requirements.txt
```
pip install sanic inflection
```

### 使用
- 目前建议直接修改demo
- PepperBot的端口，需要和go-cqhttp中设置的一致
```py
# demo文件最下方
if __name__ == "__main__":
    run(debug=True, port=53521)
```
- 开启debug，修改demo文件(及demo文件中导入的文件)时，PepperBot将会自动重启服务

### 运行
#### 使用poetry
```
poetry run python ./demos/1.py
```
#### 使用python
```
python ./demos/1.py
```

::: warning
需要同时运行go-cqhttp和PepperBot

简单来说，就是打开两个窗口，一个运行go-cqhttp，一个运行PepperBot
:::