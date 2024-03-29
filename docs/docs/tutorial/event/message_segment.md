---
title: 消息片段
---


## Text 文字

当发送连续多个Text时，PepperBot会将连续的多个Text合并为一个，以减少发送的体积

### 适配情况

QQ、微信都支持

### 用例

使用多个Text并不会自动换行，换行需要手动输入\n

```py
Text("第一行\n")
Text("第二行")
```

### api

|参数名称|类型|默认值|说明|
| :---: | :---: | :---: | :---: |
|content|str|无| 该文字消息的内容|

## At

### 适配情况

目前仅支持QQ

### 用例

传入字符串形式的QQ号或者微信号即可

```py
At("123456")
At("wxid123456")
```

### api

|参数名称|类型|默认值|说明|
| :---: | :---: | :---: | :---: |
|user_id|str|无| |

## Image 图片

可以发送本地图片或者链接

### 适配情况

QQ、微信都支持

仅QQ支持闪照

可爱猫仅支持通过url发送图片，不支持本地文件

### 用例

发送网络图片

```py
Image("http://i1.piimg.com/567571/fdd6e7b6d93f1ef0.jpg")
```

发送本地图片

```py
Image("file:///C:\\Users\\Richard\\Pictures\\1.png")
```

QQ中发送闪照

```py
await bot.group_message(
    Image(path).onebot_to_flash(),
    Text("Hello, world!"),
)
```

QQ中接受闪照，将其转变为普通图片再转发

```py
img = chain.images[0] # 假定发送了一张闪照，不然images为空列表
normalized_img = img.onebot_un_flash()

await bot.group_message(
    normalized_img,
    Text("Hello, world!"),
)
```

### api

|参数名称|类型|默认值|说明|
| :---: | :---: | :---: | :---: |
|file_path|str|无| url或者本地文件 |
|mode|str|None| 可以为flash，不建议直接修改，通过to/un_flash修改 |

## Poke 戳一戳

### 适配情况

仅QQ支持

### 用例

```py
Poke("123456")
```

## Audio 语音

### 适配情况

仅QQ支持

微信的语音消息，其实就是文件，可爱猫不支持

### 用例

url或者本地文件，用法同Image

注意，如果使用go-cqhttp，ffmpeg需要在环境变量中(可以访问到ffmpeg的可执行文件)

```py
Audio(path)
```

## Video 视频

### 适配情况

go-cqhttp不管发送本地还是网络视频都存在问题，见[ISSUE](https://github.com/Mrs4s/go-cqhttp/issues/577)

可爱猫仅支持通过url发送视频

### 用例

url或者本地文件，用法同Image

注意，如果使用go-cqhttp，ffmpeg需要在环境变量中(可以访问到ffmpeg的可执行文件)

```py
Video(path)
```

## Music 音乐

### 适配情况

目前仅支持QQ

### 用例

需要提供音乐id，id是和平台相关的，同一首歌，在不同平台上，id也会不同

```py
Music("28949129", "163")
```
