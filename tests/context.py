from typing import Dict


context = {"a": 1}


def redefine_context(context: Dict):
    print(context)
    # context.clear()
    context.update({"a": 4, "c": 3})

    # 不要重新赋值context，因为context实质上是一个指向全局context的引用
    # 如果重新赋值，则context变为了本地变量，而不是从外部传入的那个
    context = {"b": 2}

    print(context)


redefine_context(context)
print(context)
