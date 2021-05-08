import inspect


def get_current_function_name():
    return inspect.currentframe().f_back.f_code.co_name
