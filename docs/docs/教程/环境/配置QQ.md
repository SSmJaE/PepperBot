:::info
可以参考 go-cqhttp 的[官方文档](https://docs.go-cqhttp.org/guide/quick_start.html#%E5%9F%BA%E7%A1%80%E6%95%99%E7%A8%8B)
:::

## 安装

-   在[go-cqhttp](https://github.com/Mrs4s/go-cqhttp/releases)的 Github 仓库中下载符合自己操作系统的版本
-   比如 windows 10，下载 windows_amd64.exe 即可

## 初始化

:::info
可以按照自己的操作习惯，将 go-cqhttp 放在不同目录，不用和教程保持一致
:::

-   在项目下新建 onebot 文件夹，将 go-cqhttp 的可执行文件放入其中
-   运行一次

```sh
cd ./onebot
./go-cqhttp_xxxxx.exe
```

-   第一次运行时，我们选择`http通信`和`反向Websocket通信`，之后会生成 config.yml，我们需要手动修改

## 修改 config.yml

-   修改`uin`为自己的 qq 号
-   修改`password`为密码
-   修改`post_format`为`array`
-   修改`ws_reverse_servers`中
    -   修改`universal`为`ws://127.0.0.1:端口/onebot/ws`
    -   端口需要和 PepperBot 中的端口保持一致
    -   ws 的地址，我们可以在 PepperBot 中自定义，不过都需要和 go-cqhttp 保持一致

## 再次运行
