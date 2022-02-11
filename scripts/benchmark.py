# 100_0000 bot实例创建
# time
# memory

import inspect
import ast
import astpretty


def a():
    if 1:
        return True
    else:
        return False
    pass




module = ast.parse(inspect.getsource(a))
astpretty.pprint(module)
