
`PepperBot`的available

选择将缓存，缓存在单独的dict里，而不是class上，是因为，直接缓存在class上，想要获取class实例比较麻烦，

因为pepperbot存在很多运行前(可以理解为编译期)AST检查，此时，class一般还没有实例化，可能会遇到问题
