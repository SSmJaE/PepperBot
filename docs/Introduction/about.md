## 后端
- 也就是负责与QQ通信的“无头QQ”，
- 一般建议使用go-cqhttp作为“后端”

## 业务逻辑框架
> 为什么说PepperBot是一个业务逻辑框架？
- PepperBot并没有实现与QQ通信的能力，只负责处理“业务逻辑”
- PepperBot通过与后端的通信，实现了与QQ的通信
- PepperBot基于OneBot协议，所以所有符合OneBot标准的“后端”，都可以使用


