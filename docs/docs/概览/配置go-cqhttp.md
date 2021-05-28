:::info
可以参考go-cqhttp的[官方文档](https://docs.go-cqhttp.org/guide/quick_start.html#%E5%9F%BA%E7%A1%80%E6%95%99%E7%A8%8B)
:::
## 安装
- 在[go-cqhttp](https://github.com/Mrs4s/go-cqhttp/releases)的Github仓库中下载符合自己操作系统的版本

## 初始化
:::info
可以按照自己的操作习惯，将go-cqhttp放在不同目录，不用和教程保持一致
:::
- 在项目下新建backend文件夹，将go-cqhttp的可执行文件放入其中
- 运行一次
```
cd ./backend
./go-cqhttpxxxxx.exe
```
- 第一次运行时，go-cqhttp自动生成config.hjson文件，我们需要修改配置
## 修改hjson
- 修改`uin`为自己的qq号
- 修改`password`为密码
- 修改`post_message_format`为`array`
- 修改`ws_reverse_servers`中
  - `enabled`为`true`
  - 修改`reverse_url`为`ws://127.0.0.1:端口/cqhttp/ws`
  - 端口需要和PepperBot中的端口保持一致
## 再次运行

